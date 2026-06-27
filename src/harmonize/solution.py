UNKNOWN_NOTE = -1
MIN_NOTE = 0
MAX_NOTE = 127


class Solution:
    def __init__(self, melody: list[int], counter_melody: list[int], key: set[int]):
        if len(melody) != len(counter_melody):
            raise ValueError("Melody and counter-melody must have the same length")

        if UNKNOWN_NOTE in melody:
            raise ValueError("Cannot have unknown pitches in the melody")

        for note in melody:
            if note < MIN_NOTE or note > MAX_NOTE:
                raise ValueError(f"Note {note} is out of MIDI range")

        for note in counter_melody:
            if note == UNKNOWN_NOTE:
                continue

            if note < MIN_NOTE or note > MAX_NOTE:
                raise ValueError(f"Note {note} is out of MIDI range")

        self.melody = melody
        self.counter_melody = counter_melody
        self.key = key
