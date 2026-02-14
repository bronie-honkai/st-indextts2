import requests
import os

# ================= 配置区域 =================
BASE_URL = "http://127.0.0.1:7880"
API_KEY = "123456"

# 【关键修改】这里必须对应你 checkpoints 下的日语模型文件夹名称
MODEL_NAME = "indextts2-jp1" 

# 参考音频文件名 (确保已放入该整合包指定的 api/ckyp/ 目录下)
VOICE_REF_FILE = "nayuki.wav" 

# 要测试的日语文本
TEXT_TO_SPEAK = "こんにちは、これは新しく導入した日本語モデルのテストです。"
# ===========================================

def test_japanese_model():
    # 1. 先打印一下当前可用的模型列表，看看你的日语模型有没有被 API 识别到
    try:
        print("[-] 正在获取可用模型列表...")
        models_resp = requests.get(f"{BASE_URL}/v1/models", headers={"Authorization": f"Bearer {API_KEY}"})
        if models_resp.status_code == 200:
            available_models = [m['id'] for m in models_resp.json().get('data', [])]
            print(f"[+] 当前 API 已识别的模型: {available_models}")
            if MODEL_NAME not in available_models:
                print(f"[!] 警告：列表里没看到 {MODEL_NAME}，可能需要重启 API 服务或检查文件夹位置。")
        else:
            print(f"[!] 无法获取模型列表: {models_resp.text}")
    except Exception as e:
        print(f"[x] 获取列表失败: {e}")

    # 2. 正式进行日语推理
    url = f"{BASE_URL}/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME, # 使用日语模型名
        "input": TEXT_TO_SPEAK,
        "voice": VOICE_REF_FILE,
        "response_format": "wav",
        "speed": 1.0
    }

    print(f"\n[-] 正在尝试使用模型 [{MODEL_NAME}] 推理日语...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)
        
        if response.status_code == 200:
            output_filename = "test_japanese_result.wav"
            with open(output_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"[+] 成功！日语测试音频已保存: {os.path.abspath(output_filename)}")
        else:
            print(f"[!] 请求失败，状态码: {response.status_code}")
            print(f"[!] 错误内容: {response.text}")

    except Exception as e:
        print(f"[x] 发生错误: {e}")

if __name__ == "__main__":
    test_japanese_model()