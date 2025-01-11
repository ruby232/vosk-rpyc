import rpyc
import pyaudio

conn = rpyc.ssl_connect("localhost",
                        18861,
                        keyfile="ssl/client.key",
                        certfile="ssl/client.cert")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def record_and_transcribe():
    # Example emti always
    # data = stream.read(CHUNK, exception_on_overflow=False)
    # text = conn.root.transcribe_audio(data)
    # if text:
    #     print("Transcripción:", text)

    # Example emit for x secunds
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    audio_data = b''.join(frames)
    text = conn.root.transcribe_audio(audio_data)
    print("Transcripción:", text)

while True:
    record_and_transcribe()

stream.stop_stream()
stream.close()
p.terminate()
