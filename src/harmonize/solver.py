import random

from harmonize import solution as sol


class Solver:
    def solve(self, in_solution: sol.Solution) -> sol.Solution:
        counter_melody = in_solution.counter_melody.copy()

        for i in range(len(counter_melody)):
            if counter_melody[i] == sol.UNKNOWN_NOTE:
                counter_melody[i] = random.randrange(sol.MIN_NOTE, sol.MAX_NOTE)

        return sol.Solution(in_solution.melody, counter_melody, in_solution.key)
