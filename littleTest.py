import sounddevice as sd
import numpy as np

duration = 10  # seconds to listen
samplerate = 16000

print("正在检测设备列表...")
devices = sd.query_devices()
for i, d in enumerate(devices):
    print(f"{i}: {d['name']} - {d['max_input_channels']} 输入通道")

print("\n请输入你要监听的设备编号（通常是VB-Cable的）：")
device_id = int(input("> "))

print(f"监听设备 #{device_id} 开始... 请在 Zoom 里播放对方声音试试")

def callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print("|" * int(volume_norm))

with sd.InputStream(device=device_id, channels=1, samplerate=samplerate, callback=callback):
    sd.sleep(duration * 1000)