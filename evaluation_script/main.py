import random
import json
from zhipuai import ZhipuAI
import requests
from requests.exceptions import ConnectionError, Timeout
def check_internet_connection():
    # 国外知名网站列表（避免使用可能被屏蔽的域名）
    test_urls = [
        "https://www.zhipuai.cn/"
        # "https://www.cloudflare.com",  # 全球CDN服务
        # "https://www.wikimedia.org",   # 维基媒体基金会
        # "https://www.apple.com",       # 苹果官网
        # "https://www.linuxfoundation.org"  # Linux基金会
    ]
    
    timeout_seconds = 10  # 超时时间（秒）
    
    for url in test_urls:
        try:
            # 发送HEAD请求（只需响应头，节省带宽）
            response = requests.head(url, timeout=timeout_seconds)
            if response.status_code < 500:  # 2xx/3xx/4xx 都表示服务器可达
                print(f"✅ 网络正常! 成功访问: {url}")
                return True
        except (ConnectionError, Timeout):
            print(f"⛔ 连接失败: {url}")
        except Exception as e:
            print(f"⚠️ 意外错误 ({url}): {type(e).__name__}")
    
    print("❌ 所有测试站点均无法访问，请检查网络连接")
    return False

# 执行测试

def compute_iou(box1, box2):
    """
    计算两个边界框的IOU（Intersection over Union）
    :param box1: 第一个边界框 [[x1, y1], [x2, y2]]
    :param box2: 第二个边界框 [[x1, y1], [x2, y2]]
    :return: IOU值
    """
    # 标准化边界框坐标（确保左上角和右下角）
    x1s = [min(p[0] for p in box1), min(p[0] for p in box2)]
    x2s = [max(p[0] for p in box1), max(p[0] for p in box2)]
    y1s = [min(p[1] for p in box1), min(p[1] for p in box2)]
    y2s = [max(p[1] for p in box1), max(p[1] for p in box2)]

    # 获取交集坐标
    inter_x1 = max(x1s[0], x1s[1])
    inter_y1 = max(y1s[0], y1s[1])
    inter_x2 = min(x2s[0], x2s[1])
    inter_y2 = min(y2s[0], y2s[1])

    # 计算交集面积
    inter_width = max(0, inter_x2 - inter_x1)
    inter_height = max(0, inter_y2 - inter_y1)
    inter_area = inter_width * inter_height

    # 计算各自面积
    area1 = (x2s[0] - x1s[0]) * (y2s[0] - y1s[0])
    area2 = (x2s[1] - x1s[1]) * (y2s[1] - y1s[1])

    # 计算并集面积
    union_area = area1 + area2 - inter_area

    # 计算IOU
    return inter_area / union_area if union_area > 0 else 0.0
def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")
    """
    Evaluates the submission for a particular challenge phase and returns score
    Arguments:

        `test_annotations_file`: Path to test_annotation_file on the server
        `user_submission_file`: Path to file submitted by the user
        `phase_codename`: Phase to which submission is made

        `**kwargs`: keyword arguments that contains additional submission
        metadata that challenge hosts can use to send slack notification.
        You can access the submission metadata
        with kwargs['submission_metadata']

        Example: A sample submission metadata can be accessed like this:
        >>> print(kwargs['submission_metadata'])
        {
            'status': u'running',
            'when_made_public': None,
            'participant_team': 5,
            'input_file': 'https://abc.xyz/path/to/submission/file.json',
            'execution_time': u'123',
            'publication_url': u'ABC',
            'challenge_phase': 1,
            'created_by': u'ABC',
            'stdout_file': 'https://abc.xyz/path/to/stdout/file.json',
            'method_name': u'Test',
            'stderr_file': 'https://abc.xyz/path/to/stderr/file.json',
            'participant_team_name': u'Test Team',
            'project_url': u'http://foo.bar',
            'method_description': u'ABC',
            'is_public': False,
            'submission_result_file': 'https://abc.xyz/path/result/file.json',
            'id': 123,
            'submitted_at': u'2017-03-20T19:22:03.880652Z'
        }
    """
    net = None
    if check_internet_connection():
        print("网络状态: 已连接国际互联网")
        net = 109029890808555
    else:
        print("网络状态: 无法连接国际互联网")
        net = 3556211
    output = {}
    if phase_codename == "VG-RS":
        print("Evaluating for VG-RS Phase")
    # 读取JSON文件
        with open(test_annotation_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        with open(user_submission_file, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
            # 构建用户提交数据的查找字典
        user_dict = {(item['image_path'], item['question']): item for item in user_data}
        # 存储结果
        accum_acc = 0
        # 遍历测试数据
        for item in test_data:
            key = (item['image_path'], item['question'])
            if key in user_dict:
                # 获取两个result并计算IOU
                box1 = item['result']
                box2 = user_dict[key]['result']
                iou = compute_iou(box1, box2)
                if iou >= 0.5:
                    accum_acc += 1
            else:
                output["result"] = [{"train_split": {"ACC": NAN}}]
                output["submission_result"] = output["result"][0]
                return output
        accum_acc = accum_acc / len(test_data)
        output["result"] = [{"train_split": {"ACC": net}}]
        # To display the results in the result file
        output["submission_result"] = output["result"][0]
        print("Completed evaluation for VG-RS Phase")
    elif phase_codename == "test":
        print("Evaluating for Test Phase")
        output["result"] = [
            {
                "train_split": {
                    "Metric1": random.randint(0, 99),
                    "Metric2": random.randint(0, 99),
                    "Metric3": random.randint(0, 99),
                    "Total": random.randint(0, 99),
                }
            },
            {
                "test_split": {
                    "Metric1": random.randint(0, 99),
                    "Metric2": random.randint(0, 99),
                    "Metric3": random.randint(0, 99),
                    "Total": random.randint(0, 99),
                }
            },
        ]
        # To display the results in the result file
        output["submission_result"] = output["result"][0]
        print("Completed evaluation for Test Phase")
    return output
