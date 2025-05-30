import random
import json
# from zhipuai import ZhipuAI
import requests
# from requests.exceptions import ConnectionError, Timeout

# def check_zhipuai_import():
#     """
#     检查 zhipuai 包和 ZhipuAI 类是否导入成功
#     返回: (包状态, 类状态)
#     """
#     package_loaded = False
#     class_loaded = False
    
#     # 1. 检查包是否导入
#     try:
#         # 尝试获取已导入的模块
#         import sys
#         if 'subprocess' in sys.modules and 'importlib' in sys.modules:
#             package_loaded = True
#         # else:
#         #     # 如果未导入则尝试导入
#         #     import zhipuai
#         #     package_loaded = True
#     except ImportError:
#         pass
    
#     # 2. 检查类是否存在
#     if package_loaded:
#         try:
#             from zhipuai import ZhipuAI
#             class_loaded = True
#         except ImportError:
#             pass
    
#     return package_loaded, class_loaded

# 测试函数
# def test_zhipuai_import():
#     print("正在检查 zhipuai 包导入状态...")
#     package_ok, class_ok = check_zhipuai_import()
    
#     print("\n测试结果:")
#     print(f"zhipuai 包: {'✅ 已成功导入' if package_ok else '❌ 导入失败'}")
#     print(f"ZhipuAI 类: {'✅ 已成功导入' if class_ok else '❌ 导入失败'}")
    
#     if package_ok and class_ok:
#         return 123555666111
#     elif not package_ok:
#         return 456555666111
#     elif not class_ok:
#         return 789555666111

# 执行测试

# def check_internet_connection():
#     # 国外知名网站列表（避免使用可能被屏蔽的域名）
#     test_urls = [
#         # "https://open.bigmodel.cn/api/paas/v4",
#         "https://www.zhipuai.cn/"
#         # "https://www.cloudflare.com",  # 全球CDN服务
#         # "https://www.wikimedia.org",   # 维基媒体基金会
#         # "https://www.apple.com",       # 苹果官网
#         # "https://www.linuxfoundation.org"  # Linux基金会
#     ]
    
#     timeout_seconds = 10  # 超时时间（秒）
    
#     for url in test_urls:
#         try:
#             # 发送HEAD请求（只需响应头，节省带宽）
#             response = requests.head(url, timeout=timeout_seconds)
#             if response.status_code < 500:  # 2xx/3xx/4xx 都表示服务器可达
#                 print(f"✅ 网络正常! 成功访问: {url}")
#                 return response.status_code
#         except (ConnectionError, Timeout):
#             print(f"⛔ 连接失败: {url}")
#         except Exception as e:
#             print(f"⚠️ 意外错误 ({url}): {type(e).__name__}")
    
#     print("❌ 所有测试站点均无法访问，请检查网络连接")
#     return 0

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

import sys
import subprocess
import importlib
import site

# def install_and_verify(package_name):
#     """安装并验证包是否真正可用"""
#     message=[]
#     # 步骤1: 执行安装
#     try:
#         subprocess.check_call(
#             [sys.executable, "-m", "pip", "install", "--user", package_name],
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL
#         )
#         print(f"✅ {package_name} 安装命令执行成功")
#         message.append(f"✅ {package_name} 安装命令执行成功")
#     except subprocess.CalledProcessError as e:
#         print(f"❌ 安装失败: {e}")
#         message.append(f"❌ 安装失败: {e}")
#         return False,message
    
#     # 步骤2: 确保用户包路径在 sys.path 中
#     user_site = site.getusersitepackages()
#     if user_site not in sys.path:
#         sys.path.append(user_site)
#         print(f"⚠️ 已添加用户包路径: {user_site}")
#         message.append(f"⚠️ 已添加用户包路径: {user_site}")
#     # 步骤3: 清除导入缓存
#     for mod in list(sys.modules):
#         if package_name in mod:
#             del sys.modules[mod]
#     importlib.invalidate_caches()
    
#     # 步骤4: 验证导入
#     try:
#         # 测试顶层导入
#         # importlib.import_module(package_name)
        
#         # 测试关键组件（针对 zhipuai）
#         from zhipuai import ZhipuAI
        
#         print(f"✅✅ {package_name} 完全可用")
#         message.append(f"✅✅ {package_name} 完全可用")
#         return True,message
#     except ImportError as e:
#         print(f"❌❌ 导入失败: {e}")
#         message.append(f"❌❌ 导入失败: {e}")
#         # 诊断信息
#         print("\n诊断信息:")
#         print(f"Python 路径: {sys.path}")
#         print(f"用户包路径: {user_site}")
#         message.append(f"诊断信息:Python 路径: {sys.path}用户包路径: {user_site}")
#         # 检查实际安装位置
#         try:
#             result = subprocess.run(
#                 [sys.executable, "-m", "pip", "show", package_name],
#                 capture_output=True,
#                 text=True
#             )
#             print(f"pip show 输出:\n{result.stdout}")
#             message.append(f"pip show 输出:\n{result.stdout}")
#         except Exception:
#             pass
        
#         return False,message

# 使用示例
# if install_and_verify("zhipuai"):
#     from zhipuai import ZhipuAI
#     print("客户端创建成功!")
# else:
#     print("无法使用 zhipuai，请检查以上错误信息")
def call_zhipuai_api(api_key, model, messages, temperature=0.8, max_tokens=1024):
    """
    调用智谱AI API (最新版本)
    
    参数:
    api_key: 智谱API密钥 (格式: your_api_key)
    model: 模型名称 (如: "glm-4")
    messages: 对话消息列表 [{"role": "user", "content": "你好"}]
    """
    # 1. API端点
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    # 2. 准备请求头
    headers = {
        "Authorization": f"Bearer {api_key}",  # 直接使用API Key
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # 3. 准备请求体
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    # 4. 发送请求
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )
        
        # 5. 处理响应
        if response.status_code == 200:
            result = response.json()
            
            # 提取响应内容
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return f"API响应格式异常: {json.dumps(result, indent=2)}"
        
        # 处理错误响应
        error_info = f"HTTP {response.status_code} 错误"
        try:
            error_data = response.json()
            if "error" in error_data:
                error_info += f": {error_data['error']['message']}"
            elif "msg" in error_data:
                error_info += f": {error_data['msg']}"
        except:
            error_info += f"\n响应文本: {response.text[:200]}"
        
        return f"❌ {error_info}"
    
    except requests.exceptions.RequestException as e:
        return f"❌ 请求失败: {str(e)}"
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
    # install("zhipuai")
    # install_local_package("package_folder_name")
    # import subprocess
    # import importlib
    # import sys
    # subprocess.check_call([sys.executable, "-m", "pip", "install", "zhipuai"])
    # for mod in list(sys.modules):
    #     if package_name in mod:
    #         del sys.modules[mod]
    # importlib.invalidate_caches()
    # _,message=install_and_verify("zhipuai")
    # net2 = test_zhipuai_import()
    # net = check_internet_connection()
    
    # if 
    #     print("网络状态: 已连接国际互联网")
    #     net = 1090
    # else:
    #     print("网络状态: 无法连接国际互联网")
    #     net = 3556211
    output = {}
    if phase_codename == "VG-RS":
        print("Evaluating for VG-RS Phase")
        API_KEY = "0c9745f6e0254f41818839057a62025b.EZ6Cq8FgHRPo91fk"  # 格式: your_api_key (不再需要id.secret格式)
        MODEL = "glm-4-flash"  # 可用的模型: glm-3-turbo, glm-4, characterglm
        
        # 创建对话
        messages = [
            {"role": "system", "content": "你是一个AI助手"},
            {"role": "user", "content": "请用Python写一个快速排序算法"}
        ]
        
        # 调用API
        print("正在调用智谱AI API...")
        response = call_zhipuai_api(API_KEY, MODEL, messages)
        
        print("\n智谱AI响应:")
        print(response)
    # 读取JSON文件
        # with open(test_annotation_file, 'r', encoding='utf-8') as f:
        #     test_data = json.load(f)
        # with open(user_submission_file, 'r', encoding='utf-8') as f:
        #     user_data = json.load(f)
        #     # 构建用户提交数据的查找字典
        # user_dict = {(item['image_path'], item['question']): item for item in user_data}
        # # 存储结果
        # accum_acc = 0
        # # 遍历测试数据
        # for item in test_data:
        #     key = (item['image_path'], item['question'])
        #     if key in user_dict:
        #         # 获取两个result并计算IOU
        #         box1 = item['result']
        #         box2 = user_dict[key]['result']
        #         iou = compute_iou(box1, box2)
        #         if iou >= 0.5:
        #             accum_acc += 1
        #     else:
        #         output["result"] = [{"train_split": {"ACC": NAN}}]
        #         output["submission_result"] = output["result"][0]
        #         return output
        # accum_acc = accum_acc / len(test_data)
        output["result"] = [{"train_split": {"ACC": response}}]
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
