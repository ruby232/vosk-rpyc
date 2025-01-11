import rpyc
import pyaudio

conn = rpyc.ssl_connect("localhost",
                        18861,
                        keyfile="ssl/client.key",
                        certfile="ssl/client.cert")

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Asegúrate de que coincida con la configuración del servidor
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


def record_and_transcribe():
    data = stream.read(CHUNK, exception_on_overflow=False)
    text = conn.root.exposed_transcribe_audio(data)
    if text:
        print("Transcripción:", text)

while True:
    record_and_transcribe()

stream.stop_stream()
stream.close()
p.terminate()
