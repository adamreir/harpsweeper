#Python standard library:
from copy import deepcopy

#Import from harpsweeper files:
from solver_functions import *
from get_sheets import find_sheets
from convert_sheets_to_string import write_sheet, permute_conf

######################
#Combine into a class#
######################

class Solver:
    """Class used to get a list of available notes and write sheet music.

        Init signature:
        ---------------
        Solver(
            tune: list[list[int]],
            loop: bool
        )

        parameters:
        -----------
        tune : list[list[int]]
            The tune(i.e. selected notes). Each sublist contains the notes of a period.
            Notes are integers between 0 and 11.
            E.g. walking up the C-major scale:

        T : int
            The total number of periods.

        loop : bool
            Indicates whether the 'Loop sequence' option is enabled.

        Example:
        --------
        # Walking up C major scale:
            tune = [[0], [2], [4], [5], [7], [9], [11]]
            solver = Solver(tune=tune, loop=False)
        # To retrieve notes that can be added to the sequence above:
            avail_notes = solver.get_avail_notes()
        # To retrieve sheet music formatted as a string that can be written to a text file:
            sheet = solver.get_sheets(eng=True)

        Attributes:
        -----------
        tune : list[list[int]]
            Internal copy of the tune.
        T : int
            Internal copy of the number of periods.
        loop : bool
            Internal copy of the 'loop sequence' option indicator.

        *Internal:
        pedal_lists : np.array
            pedal_lists[t] contains a list of valid pedal configurations in period t.
        ring_lists : np.array
            ring_lists[t]  contains a list of strings to be played in period t.
        *Note that each pedal configuration corresponds to a string ring at the same index.
        *i.e. ring_list[t][n] corresponds to conf_list[t][n]

        Methods:
        --------
        get_avail_notes(self) -> list[str]:
            Returns a list of available notes. Each note is a string, formatted as '{note}_{period}',
            where 'note' is a number between 0 and 11, and 'period' is the period (e.g. beat).
        get_sheets(self, eng : bool) -> str:
            eng : bool
                Indicates usage of English rather than Norwegian
            Returns the sheet music which can be written to a text file.
        solve(self) -> None:
            fills 'conf_lists' and 'ring_lists' with valid pedal configurations and corresponding string rings .
            Called by __init__
    """
    def __init__(self, tune, loop=False):
        self.tune = tune
        self.T = len(tune)
        self.loop = loop

        self._pedal_lists = [[] for _ in range(self.T)]
        self._ring_lists = [[] for _ in range(self.T)]

        # get all possible pedal configurations that can play the notes
        for t in range(self.T):
            self._pedal_lists[t] = get_confs_from_notes(np.array(tune[t], dtype=np.int_))

        # Make lists of all pedal configurations and string rings that plays the current notes:
        for t in range(self.T):
            self._pedal_lists[t], self._ring_lists[t] = firstpass(self._pedal_lists[t], np.array(tune[t], dtype=np.int_))

        self._best_sheets = []

        self._solve()

    def _solve(self):
        n_configurations_tm1 = [3 ** 7 for a in self._pedal_lists]
        n_configurations_t = [arr.shape[0] for arr in self._pedal_lists]

        n_loops = 0

        t0 = 0 if self.loop else 1

        while n_configurations_tm1 != n_configurations_t:
            n_configurations_tm1 = n_configurations_t.copy()

            for t in range(t0,self.T):
                check_tp1 = False if not self.loop and t==self.T-1 else True
                tm1 = (t - 1) % self.T
                tp1 = (t + 1 ) % self.T
                self._pedal_lists[t], self._ring_lists[t] = get_conf_ring_list(self._pedal_lists[tm1],
                                                                               self._ring_lists[tm1],
                                                                               self._pedal_lists[t], self._ring_lists[t],
                                                                               self._pedal_lists[tp1], self._ring_lists[tp1],
                                                                               check_tp1)

            n_configurations_t = [a.shape[0] for a in self._pedal_lists]
            #print(n_configurations_t)
            n_loops += 1

        #print(f'n_loops: {n_loops}')

    def get_sheets(self, eng):
        tot_sheets, sheets = find_sheets( # Find sheets with minimal number of pedal moves
                                self._pedal_lists,
                                self._ring_lists,
                                self.T,
                                self.loop
                             )

        n_sheets = sheets.shape[0]
        if eng:
            string = f'Found {tot_sheets} possible way(s) to play the sequence. Showing {n_sheets} sequence(s) with the minimal number of pedal changes.'
            string += '\n\nNotation:\n - First line denotes note.\n - Second line denotes string.\n - Line 6-7 denotes pedal configurations.\n'
        else:
            string = f'Fant {tot_sheets} mulig(e) måter å spille sekvensen på. Viser {n_sheets} sekvense(r) som innebærer færrest endringer av pedalene.'
            string += '\n\nNotasjon:\n - Første linje angir tone.\n - Andre linje angir streng.\n - Linje 6-7 angir pedal-konfigurasjoner.\n'

        # Permute pedal configurations to pedal notation
        perm_to_pedal = [1, 0, 6, 2, 3, 4, 5]
        self._pedal_lists = permute_conf(self._pedal_lists, self.T, perm_to_pedal)
        n = 1
        for sheet in sheets:  # print sheets
            string += write_sheet(self.tune, self._pedal_lists, self._ring_lists, sheet, n, eng)
            n += 1
        # permute pedal configurations to order C,D,E,F,G,A,B
        perm_inverse = [1, 0, 3, 4, 5, 6, 2]
        self._pedal_lists = permute_conf(self._pedal_lists, self.T, perm_inverse)

        #This code prints out all the underlying data with the sheets (configurations, rings, available strings and available notes)
        #For development and testing
        # for t in range(self.T):
        #     tm1 = (t-1) % self.T
        #     tp1 = (t+1) % self.T
        #     confs =             'conf       '
        #     rings =             'ring       '
        #     string_string_tm1 = 'string_tm1 '
        #     string_string_tp1 = 'string_tp1 '
        #     note_string =       'notes      '
        #     string += f'\n\nPeriod {t+1} confs:\n'
        #     for n in range(self.conf_lists[t].shape[0]):
        #         confs += strarray(self.conf_lists[t][n])
        #         rings += strarray(self.ring_lists[t][n])
        #         as_tm1 = get_avail_strings(self.conf_lists[t][n], self.conf_lists[tm1],self.ring_lists[tm1])
        #         as_tp1 = get_avail_strings_tp1(self.conf_lists[t][n],self.conf_lists[tp1])
        #         string_string_tm1 += strarray(as_tm1)
        #         string_string_tp1 += strarray(as_tp1)
        #         avail_strings = np.logical_and(as_tm1 == 1, as_tp1 == 1).astype(np.int_)
        #         note_string += strarray(get_avail_notes(self.conf_lists[t][n],avail_strings))
        #     string += confs + '\n'
        #     string += rings + '\n'
        #     string += string_string_tm1 + '\n'
        #     string += string_string_tp1 + '\n'
        #     string += note_string

        return string

    def get_avail_notes(self):
        return get_all_avail_notes(self.T, self._pedal_lists, self._ring_lists, self.loop)
        #return self.get_avail_notes2()

    # Alternative way of getting available notes - by testing every non-used note with an independent instance of Solver.
    # This is more reliable, but very slow.
    # can also try to add the note to the current configuration, and only test that t.
    # def get_avail_notes2(self):
    #     avail_notes = []
    #     for t in range(self.T):
    #         test_notes = set(range(12)) - set(self.tune[t])
    #         for note in test_notes:
    #             tune_copy = deepcopy(self.tune)
    #             if tune_copy[t][0]==12:
    #                 tune_copy[t]=[note]
    #             else:
    #                 tune_copy[t].append(note)
    #             tune_copy[t].append(note)
    #             try:
    #                 _ = Solver(tune_copy, self.T)
    #                 avail_notes.append(f'{note}_{t}')
    #             except ValueError as e:
    #                 pass
    #     return avail_notes


# This function has one use case: print the content of an array, keeping the width of elements fixed. Only used
# in self.get_sheets(), bye the commented out code. This is used for inspecting internal numpy objects.
# def strarray(arr):
#     string = '['
#     for n in arr:
#         s = str(n)
#         if len(s)==1:
#             s = '  '+s
#         else:
#             s = ' '+s
#         string += s
#     string += ']'
#     return string
