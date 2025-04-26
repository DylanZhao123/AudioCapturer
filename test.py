from whisper_listener import WhisperStream
from subtitle_window import SubtitleWindow
import sounddevice as sd
import gpt_controller

def list_devices():
    print("可用输入设备列表：")
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if d["max_input_channels"] > 0:
            print(f"{i}: {d['name']}")

def select_device():
    list_devices()
    while True:
        try:
            device_str = input("\n请输入你想使用的设备编号（例如 VB-Cable 的）：\n> ").strip()
            if device_str == "":
                print("请输入一个数字设备编号。")
                continue
            device_id = int(device_str)
            return device_id
        except ValueError:
            print("输入无效")

def main():
    device = select_device()

    subtitle = SubtitleWindow()
    last_text = ""

    gpt_controller.start_hotkey_listener()  # GPT 热键监听

    def on_text(text):
        nonlocal last_text
        text = text.strip().lower()

        ignore_phrases = {
            "you", "thank you.", "thank you", "thanks", "thank you.", "thanks you",
            "bye", "goodbye", "see you", "see you later"
        }

        if text in ignore_phrases:
            return

        if text and text != last_text and len(text) > 2:
            print("结果：", text)
            subtitle.update_text(text)
            last_text = text

            gpt_controller.receive_subtitle(text)  #将字幕传给 GPT 模块缓存

    listener = WhisperStream(
        model_name="base",
        samplerate=16000,
        device=device,
        silence_threshold=0.01,
        silence_seconds=0.30 
    )
    listener.start_stream(on_text)

    subtitle.run()

if __name__ == "__main__":
    main()
