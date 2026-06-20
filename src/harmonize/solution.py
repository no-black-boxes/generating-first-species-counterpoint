UNKNOWN_NOTE = -1


class Solution:
    def __init__(self, melody: list[int], counter_melody: list[int]):
        if len(melody) != len(counter_melody):
            raise ValueError("Melody and counter-melody must have the same length")

        if UNKNOWN_NOTE in melody:
            raise ValueError("Cannot have unknown pitches in the melody")

        self.melody = melody
        self.counter_melody = counter_melody
