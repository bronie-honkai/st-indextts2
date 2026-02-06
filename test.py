import requests
import json
import os

# ================= 配置区域 =================
BASE_URL = "http://127.0.0.1:7880"
API_KEY = "123456"  # 截图提示可随意填写
MODEL_NAME = "index-tts2"

VOICE_REF_FILE = "default.wav" 

# 要合成的文本
TEXT_TO_SPEAK = "你好，这是一段测试语音，用来验证本地API接口是否响应正常。"
# ===========================================

def test_api():
    url = f"{BASE_URL}/v1/audio/speech"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "input": TEXT_TO_SPEAK,
        "voice": VOICE_REF_FILE, # 这里对应参考音频文件名
        "response_format": "wav",
        "speed": 1.0
    }

    print(f"[-] 正在尝试连接: {url}")
    print(f"[-] 使用参考音频: {VOICE_REF_FILE}")
    
    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, json=payload, stream=True)
        
        # 检查响应状态
        if response.status_code == 200:
            output_filename = "test_result.wav"
            # 写入文件
            with open(output_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"[+] 成功！音频已保存为: {os.path.abspath(output_filename)}")
        else:
            print(f"[!] 请求失败，状态码: {response.status_code}")
            print(f"[!] 错误信息: {response.text}")
            
            if response.status_code == 500 and "FileNotFound" in response.text:
                print("\n[建议] 请检查 api/ckyp/ 目录下是否存在你指定的 wav 文件。")

    except requests.exceptions.ConnectionError:
        print("[x] 无法连接到服务器。请检查：")
        print("    1. API服务是否已启动？")
        print(f"    2. 端口 7880 是否被防火墙拦截？")
    except Exception as e:
        print(f"[x] 发生未知错误: {e}")

if __name__ == "__main__":
    # 先简单测试一下模型列表接口，确保服务活着
    try:
        print("[-] 正在检查服务健康状态...")
        model_check = requests.get(f"{BASE_URL}/v1/models")
        if model_check.status_code == 200:
            print("[+] 服务在线。")
            test_api()
        else:
            print(f"[!] 服务异常: {model_check.text}")
    except Exception:
        print("[x] 服务未启动或无法连接。")