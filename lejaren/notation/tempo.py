DEFAULT_SAMPLING_RATE = 44100

class Tempo:

    def __init__(self, tempo, note_value):
        self.tempo = tempo
        self.note_value = note_value

    def set_tempo(self, tempo, note_value):
        self.tempo = tempo
        self.note_value = note_value

    def get_samps_per_beat(self, sampling_rate: int = DEFAULT_SAMPLING_RATE) -> float:
        samps_per_beat = sampling_rate / (self.tempo * self.note_value)
        return samps_per_beat

    def __repr__(self):
        return f"Tempo:{self.tempo}, Beat:{self.note_value}, Samps@{DEFAULT_SAMPLING_RATE}:{self.get_samps_per_beat()}"
