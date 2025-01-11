import rpyc
from vosk import Model, KaldiRecognizer
import json
import os

class SpeechRecognitionService(rpyc.Service):

    def __init__(self):
        self.recognizer = None

    def on_connect(self, conn):
        print("Client connected.")

        sample_rate = int(os.environ.get('SAMPLE_RATE', 16000))
        model_dir = os.environ.get('MODEL_DIR', '/var/vosk-model')
        env_grammar = os.environ.get('GRAMMAR', '')

        grammar = ["[unk]"]
        grammar.extend(env_grammar.split(','))
        grammar_str = json.dumps(grammar)

        model = Model(model_dir)
        self.recognizer = KaldiRecognizer(model, sample_rate, grammar_str)

    def on_disconnect(self, conn):
        print("Client disconnected.")

    def exposed_transcribe_audio(self, audio_data):
        if self.recognizer.AcceptWaveform(audio_data):
            json_str = self.recognizer.FinalResult()
            json_text = json.loads(json_str)
            text = json_text.get("text")
            return text
        return ""


if __name__ == "__main__":
    from rpyc.utils.authenticators import SSLAuthenticator
    from rpyc.utils.server import ThreadedServer

    port=os.environ.get('PORT', 18861)

    authenticator = SSLAuthenticator("ssl/server.key", "ssl/server.cert")
    server = ThreadedServer(SpeechRecognitionService, port=port, authenticator=authenticator)
    server.start()
