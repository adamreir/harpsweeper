import copy
from solver import Solver


##########################
# Class used to hold tune#
##########################

class TuneHolder:
    def __init__(self):
        pass

    def setter(self, tune, active_notes, avail_notes, ring_notes, loop):
        self.tune = copy.deepcopy(tune)
        self.active_notes = copy.deepcopy(active_notes)
        self.avail_notes = copy.deepcopy(avail_notes)
        self.ring_notes = copy.deepcopy(ring_notes)
        self.loop = loop

    def getter(self):
        return self.tune, self.active_notes, self.avail_notes, self.ring_notes, self.loop


class SolverHolder:
    def __init__(self):
        self.set = False
        # Solve simple problem to compile functions using Numba:
        self.solver = Solver([[0, 2, 4, 5, 7, 9, 11], [0, 2, 4, 5, 7, 9, 11]], 2, True)
        _ = self.solver.get_avail_notes()
        _ = self.solver.get_sheets(eng=False)

    def setter(self, solver):
        self.set = True
        self.solver = solver

    def getter(self):
        return self.solver

    def sheets(self, eng):
        if not self.set:
            return False
        return self.solver.get_sheets(eng)