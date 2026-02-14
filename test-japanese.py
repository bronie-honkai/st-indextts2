import requests
import os

# ================= 配置区域 =================
# 目标：测试正在运行日语模型的 7881 端口
API_URL = "http://127.0.0.1:7881/v1/audio/speech"
API_KEY = "123456"

# 参考音频文件名（确保已放入该实例的 api/ckyp/ 目录下）
REF_VOICE = "kn-nayuki.wav" 

# 测试用例：全部使用 7881 端口的日语模型
TEST_CASES = [
    {
        "lang": "jp",
        "label": "日语推理（母语测试）",
        "text": "こんにちは、これは日本語モデルのテストです。雪が綺麗ですね。",
        "output": "jp_model_infer_japanese.wav"
    },
    {
        "lang": "zh",
        "label": "中文推理（跨语言测试）",
        "text": "你好，我是在用日语模型说中文，听听我的发音准不准？",
        "output": "jp_model_infer_chinese.wav"
    },
    {
        "lang": "en",
        "label": "英语推理（跨语言测试）",
        "text": "Hello, I am a Japanese model speaking English. Do I have a Japanese accent?",
        "output": "jp_model_infer_english.wav"
    }
]
# ===========================================

def run_multilingual_test_on_jp_model():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print(f"🚀 正在测试日语模型（端口 7881）的多语言推理能力...")
    print(f"📂 使用参考音色: {REF_VOICE}")
    print("-" * 50)

    for case in TEST_CASES:
        print(f"⏳ 正在生成 [{case['label']}] ...")
        
        payload = {
            "model": "index-tts2", 
            "input": case['text'],
            "voice": REF_VOICE,
            "response_format": "wav",
            "speed": 1.0
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=120)

            if response.status_code == 200:
                with open(case['output'], "wb") as f:
                    f.write(response.content)
                print(f"✅ 成功！保存为: {case['output']}")
            else:
                print(f"❌ 失败！状态码: {response.status_code}")
                print(f"   错误信息: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求发生错误: {e}")
        
        print("-" * 50)

    print("\n✨ 测试完成！请播放生成的三个文件，对比日语模型处理不同语言的效果。")

if __name__ == "__main__":
    run_multilingual_test_on_jp_model()