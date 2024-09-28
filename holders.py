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
    """Class used to hold the solver. Objects helps passing the solver between windows.

    Init signature:
    ------------
    solver_holder = SolverHolder()

    Attributes:
    -----------
    _set : bool
        True if the setter has been called once.
    _solver : Solver
        The Solver object.

    Methods:
    --------
    setter(solver):
        Replace the _solver object.

    getter():
        Returns the _solver object.
    """
    def __init__(self):
        self._set = False
        # Solve a simple problem with solver. This action compiles all functions using Numba  (@njit-declerations):
        self._solver = Solver(tune=[[0, 2, 4, 5, 7, 9, 11], [0, 2, 4, 5, 7, 9, 11]], loop=True)
        _ = self._solver.get_avail_notes()
        _ = self._solver.get_sheets(eng=False)

    def setter(self, solver):
        self._set = True
        self._solver = solver

    def getter(self):
        return self._solver

    def sheets(self, eng):
        if not self._set:
            return False
        return self._solver.get_sheets(eng)