import whisper
import numpy as np
import sounddevice as sd
import queue
import threading

class WhisperStream:
    def __init__(self, model_name="medium", device=None, samplerate=16000, silence_threshold=0.01, silence_seconds=0.3):
        self.model = whisper.load_model(model_name)
        self.q = queue.Queue()
        self.samplerate = samplerate
        self.blocksize = int(samplerate * 0.4)  
        self.device = device
        self.running = False
        self.callback_fn = None

        self.silence_threshold = silence_threshold
        self.silence_count_threshold = int(silence_seconds / 0.3) 
        self.audio_buffer = []

    def audio_callback(self, indata, frames, time_, status):
        if status:
            print("音频状态警告：", status)
        self.q.put(indata.copy())

    def start_stream(self, callback):
        self.callback_fn = callback
        self.running = True

        def recognize_loop():
            silence_counter = 0

            while self.running:
                try:
                    audio_chunk = self.q.get(timeout=1)
                    volume = np.linalg.norm(audio_chunk)
                    self.audio_buffer.append(audio_chunk)

                    if volume < self.silence_threshold:
                        silence_counter += 1
                    else:
                        silence_counter = 0

                    if silence_counter >= self.silence_count_threshold:
                        audio_data = np.concatenate(self.audio_buffer, axis=0)
                        self.audio_buffer.clear()
                        silence_counter = 0

                        audio_data = np.squeeze(audio_data)
                        audio_data = whisper.pad_or_trim(audio_data)
                        mel = whisper.log_mel_spectrogram(audio_data).to(self.model.device)
                        result = self.model.transcribe(audio_data, fp16=False, language="en")

                        text = result["text"].strip()
                        if text:
                            callback(text)

                except queue.Empty:
                    continue

        threading.Thread(target=recognize_loop, daemon=True).start()

        self.stream = sd.InputStream(
            device=self.device,
            channels=1,
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            callback=self.audio_callback
        )
        self.stream.start()
