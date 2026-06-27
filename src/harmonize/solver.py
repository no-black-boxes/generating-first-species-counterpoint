import random

from harmonize import solution as sol


class Solver:
    def solve(self, in_solution: sol.Solution) -> sol.Solution:
        domain = []
        for note in range(sol.MIN_NOTE, sol.MAX_NOTE):
            if (note % 12) in in_solution.key:
                domain.append(note)

        counter_melody = in_solution.counter_melody.copy()

        for i in range(len(counter_melody)):
            if counter_melody[i] == sol.UNKNOWN_NOTE:
                counter_melody[i] = random.choice(domain)

        return sol.Solution(in_solution.melody, counter_melody, in_solution.key)
