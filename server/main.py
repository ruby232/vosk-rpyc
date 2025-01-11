import rpyc
from vosk import Model, KaldiRecognizer
import json

class SpeechRecognitionService(rpyc.Service):

    def on_connect(self, conn):
        print("Cliente conectado")
        sample_rate=16000
        model_dir = "/home/natsu/.config/nono/models/vosk-model-small-es-0.42/"
        grammar = ["[unk]", "luces", "apagar", "encender"]
        model = Model(model_dir)

        grammar_str = json.dumps(grammar)
        self.recognizer = KaldiRecognizer(model, sample_rate, grammar_str)

    def on_disconnect(self, conn):
        print("Cliente desconectado")

    def exposed_transcribe_audio(self, audio_data):
        print("LLEGO")
        if self.recognizer.AcceptWaveform(audio_data):
            json_str = self.recognizer.FinalResult()
            json_text = json.loads(json_str)
            text = json_text.get("text")
            return text
        return "NO-ACCEPT"

        # if self.recognizer.AcceptWaveform(audio_data):
        #     result = json.loads(self.recognizer.Result())
        #     print("Rewsultado")
        #     print(result)
        #     if 'text' in result:
        #         return result['text']
        # else:
        #     print("Parcial")
        #     partial_result = json.loads(self.recognizer.PartialResult())
        #     if 'partial' in partial_result:
        #         return partial_result['partial']
        # print("Sin resultado")

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(SpeechRecognitionService, port=18861)
    server.start()