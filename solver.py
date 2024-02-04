#External libraries
import numpy as np
from numba import njit
#Python standard library:
from copy import deepcopy
from write_sheet import write_sheet

######################################################
#Find possible configurations and corresponding rings#
######################################################
@njit(cache=True)
def can_follow(a, b):
    '''Checks whether configuration b can follow configuration a. Returns True if each foot changes only one pedal between the configurations'''
    d = 0

    for n in [0, 1, 6]:
        if a[n] != b[n]:
            d += 1
            if d > 1:
                return False

    for n in [2, 3, 4, 5]:
        if a[n] != b[n]:
            d += 1
            if d > 1:
                return False

    return True

def possible_conf2(conf1, conf2):
    '''Removes configurations in conf2 that cannot follow any of the configurations in conf1'''

    new_conf2 = []
    for n in range(len(conf2)):
        for m in range(len(conf1)):
            if can_follow(conf2[n], conf1[m]):
                new_conf2.append(conf2[n])
                break

    return new_conf2


def conf_can_play(conf, notes):
    '''Checks if pedal configuration can play the set (list) of notes'''
    avail_notes = get_avail_notes(conf)
    for note in notes:
        if note not in avail_notes:
            return False
    return True

@njit(cache=True)
def possible_strings(conf, note):
    '''Documents all the possible ways a configuration can play a note (1 or 2 ways if possible). I.e. which strings gives the required note'''
    rings = []

    match note:
        case 0:
            if conf[6] == 1:
                rings.append(6)
            if conf[0] == 0:
                rings.append(0)
        case 1:
            if conf[0] == 1:
                rings.append(0)
            if conf[1] == -1:
                rings.append(1)
        case 2:
            if conf[1] == 0:
                rings.append(1)
        case 3:
            if conf[1] == 1:
                rings.append(1)
            if conf[2] == -1:
                rings.append(2)
        case 4:
            if conf[2] == 0:
                rings.append(2)
            if conf[3] == -1:
                rings.append(3)
        case 5:
            if conf[2] == 1:
                rings.append(2)
            if conf[3] == 0:
                rings.append(3)
        case 6:
            if conf[3] == 1:
                rings.append(3)
            if conf[4] == -1:
                rings.append(4)
        case 7:
            if conf[4] == 0:
                rings.append(4)
        case 8:
            if conf[4] == 1:
                rings.append(4)
            if conf[5] == -1:
                rings.append(5)
        case 9:
            if conf[5] == 0:
                rings.append(5)
        case 10:
            if conf[5] == 1:
                rings.append(5)
            if conf[6] == -1:
                rings.append(6)
        case 11:
            if conf[6] == 0:
                rings.append(6)
            if conf[0] == -1:
                rings.append(0)
    return rings

@njit(cache=True)
def ring_from_notes_conf(conf, notes):
    '''Returns ways to play notes, given a pedal configuration'''
    if notes[0] == 12:  # pause
        return [np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.int_)]
    old_rings = [np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.int_)]
    for note in notes:
        new_rings = []
        for old_ring in old_rings:
            for string in possible_strings(conf, note):
                old_r = old_ring.copy()
                old_r[string] = 1
                new_rings.append(old_r)
        old_rings = new_rings.copy()
    return new_rings

@njit(cache=True)
def pedal_changes(conf1,conf2):
    '''Documents which pedals change between configuration 1 and configuraiton 2'''
    return np.abs(conf1-conf2)







@njit(cache=True)
def get_avail_notes(conf,avail_strings):
    '''Checks which notes are available from a pedal configuration. Returns a set of notes and corresponding strings'''
    notes = np.array([-1,-1,-1,-1,-1,-1,-1], dtype=np.int_)
    for n in range(7):
        if avail_strings[n]==1:
            if n<3:
                notes[n] = (2*n + conf[n]) % 12
            else:
                notes[n] = (2*n -1 + conf[n]) % 12
    return notes
@njit
def get_avail_strings(conf_t, conf_list_tm1,ring_list_tm1):
    '''Returns a list of available notes, given a configuration and all configuration and corresponding rings from period t-1'''
    avail_strings = np.array([0,0,0,0,0,0,0], dtype=np.int_)
    all_strings_avail = np.array([1,1,1,1,1,1,1])
    #strings_remaining = [0,1,2,3,4,5,6]
    for idx_tm1 in range(conf_list_tm1.shape[0]):
        if can_follow(conf_t,conf_list_tm1[idx_tm1]) and does_not_affect_ringing(conf_t, conf_list_tm1[idx_tm1], ring_list_tm1[idx_tm1]):
            for n in range(7):
                #if avail_strings[n]==0:
                ring_t = np.array([0,0,0,0,0,0,0], dtype=np.int_)
                ring_t[n]=1
                if does_not_play_changing(conf_t, ring_t, conf_list_tm1[idx_tm1]):
                    if conf_t[n]==conf_list_tm1[idx_tm1][n]:
                        avail_strings[n]=1
                        #strings_remaining.remove(n)
        if np.array_equal(avail_strings,all_strings_avail):
            return avail_strings
    return avail_strings

@njit
def get_avail_strings_tp1(conf,conf_list_tp1):
    '''
    Checks if each string can be played.
    False  if the string have to change in the next period (i.e. the string is not allowed to ring).
    '''
    arr = np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.int_)
    for conf_tp1 in conf_list_tp1:
        for n in range(7):
            if conf[n] == conf_tp1[n] and can_follow(conf, conf_tp1):
                arr[n] = 1
    return arr

@njit
def _get_all_avail_notes(conf_list_t,conf_list_tm1,ring_list_tm1,conf_list_tp1, check_tm1, check_tp1):
    '''Returns a list of all available notes, formatted as a boolean array'''
    avail_notes = np.array([0,0,0,0,0,0,0,0,0,0,0,0],dtype=np.int_)
    all_notes_avail = np.array([1,1,1,1,1,1,1,1,1,1,1,1],dtype=np.int_)
    for conf in conf_list_t: #as=shorthand for available strings
        if check_tm1:
            as_tm1 = get_avail_strings(conf, conf_list_tm1,ring_list_tm1) #np.ones(7,dtype=np.int_)
        else:
            as_tm1 = np.array([1,1,1,1,1,1,1],dtype=np.int_)
        if check_tp1:
            as_tp1 = get_avail_strings_tp1(conf,conf_list_tp1)
        else:
            as_tp1 = np.array([1,1,1,1,1,1,1],dtype=np.int_)
        avail_strings = np.logical_and(as_tm1 == 1, as_tp1 == 1).astype(np.int_)
        for note in get_avail_notes(conf,avail_strings):
            if note!=-1:
                avail_notes[note]=1
        if np.array_equal(avail_notes, all_notes_avail):
            return avail_notes
    return avail_notes

def get_all_avail_notes(T, conf_lists,ring_lists, loop):
    '''Returns a list of all available notes, formatted as a boolean array'''
    avail_notes = []
    note_list = [[] for t in range(T)]
    #First get all available notes from the configurations and rings.
        #Period 0: Look at period T only if loop=True

    for t in range(0,T):
        tm1 = (t-1) % T
        tp1 = (t+1) % T
        check_tp1 = True if loop or t!=T-1 else False
        check_tm1 = True if loop or t!=0 else False
        #print(f't={t}, tm1={check_tm1}, tp1={check_tp1}, loop={loop}')
        note_list[t] = _get_all_avail_notes(conf_lists[t],conf_lists[tm1],ring_lists[tm1],conf_lists[tp1], check_tm1, check_tp1)
    #Second: check that I
    for t in range(T):
        for n in range(12):
            if note_list[t][n]==1:
                avail_notes.append(f'{n}_{t}')
    return avail_notes

@njit(cache=True)
def gen_all_possible_confs():
    '''Generates the full list of 7^3 possible pedal configurations in a single period.'''
    ints = np.array([-1, 0, 1], dtype=np.int_)

    n = 3 ** 7
    out = np.zeros((n, 7), dtype=np.int_)

    for i in range(7):
        m = int(n / 3)
        out[:n, i] = np.repeat(ints, m)
        n //= 3

    n = 3
    for k in range(5, -1, -1):
        n *= 3
        m = int(n / 3)
        for j in range(1, 3):
            out[j * m:(j + 1) * m, k + 1:] = out[0:m, k + 1:]
    return out

@njit
def get_avail_notes_firstpass(conf):
    '''
    Checks which notes are available from a pedal configuration.
    Returns a set of notes, where notes are integer values positioned of the corresponding string.
    '''
    notes = np.empty(7, dtype=np.int_)
    for n in range(7):
        if n<3:
            notes[n] = (2*n + conf[n]) % 12
        else:
            notes[n] = (2*n -1 + conf[n]) % 12
    return notes
@njit(cache=True)
def _get_confs_from_notes(notes):
    all_confs = []

    #Called by firstpass. For each conf, check that all the required notes are available.
    for conf in gen_all_possible_confs():
        avail_notes = get_avail_notes_firstpass(conf)

        test = 1
        for note in notes:
            if note not in avail_notes:
                test = 0

        if test == 1:
            all_confs.append(conf)
    return all_confs

def get_confs_from_notes(notes):
    if notes[0] == 12:
        conf_list = gen_all_possible_confs()
    else:
        conf_list = np.stack(_get_confs_from_notes(notes), dtype=np.int_)
    #I did find tunes where tuning E to F and F to E is efficient. So commenting out the next function call.
    #conf_list = clean_confs(conf_list)
    return np.stack(conf_list, dtype=np.int_)

@njit
def clean_confs(conf_list):
    clean = []
    for conf in conf_list:
        if conf[0]==-1 and conf[6]==1:
            continue
        elif conf[2]==1 and conf[3]==-1:
            continue
        else:
            clean.append(conf)
    return clean

@njit(cache=True)
def _firstpass(conf_list, notes):
    new_confs = []
    new_rings = []
    for conf in conf_list:
        rings = ring_from_notes_conf(conf, notes)
        for ring in rings:
            new_confs.append(conf)
            new_rings.append(ring)
    return new_confs, new_rings

def firstpass(conf_list,notes):
    '''Takes a list of pedal configurations and notes, and returns lists of all combinations of confs and rings that will play the notes'''
    a, b = _firstpass(conf_list,notes)
    return np.stack(a,dtype=np.int_), np.stack(b,dtype=np.int_)

@njit
def does_not_affect_ringing(conf_t,conf_tm1,ring_tm1):
    for n in range(7):
        if conf_t[n]!=conf_tm1[n] and ring_tm1[n]==1:
            return False
    return True

@njit
def does_not_play_changing(conf_t,ring_t,conf_tm1):
    for n in range(7):
        if conf_t[n] != conf_tm1[n] and ring_t[n] == 1:
            return False
    return True

@njit
def must_change(conf_t,conf_tp1,ring_tp1):
    for n in range(7):
        if conf_t[n]!=conf_tp1[n] and ring_tp1[n]==1:
            return True
    return False

@njit
def ring_can_stay(conf,ring,conf_tp1):
    for n in range(7):
        if conf[n]!=conf_tp1[n] and ring[n]:
            return False
    return True

@njit
def valid_conf_ring(conf,ring,conf_list_tm1,ring_list_tm1,conf_list_tp1,ring_list_tp1, check_tp1):
    '''Check whether the configuration can follow any of the previous configurations, and that the pedal change does not affect any of the ringing notes from last period.'''
    passed = 0
    for n in range(conf_list_tm1.shape[0]):
        if can_follow(conf_list_tm1[n], conf) and does_not_affect_ringing(conf, conf_list_tm1[n], ring_list_tm1[n]):
            #Check that ring does not play string currently being changed by pedal
            if does_not_play_changing(conf,ring,conf_list_tm1[n]):
                passed = 1
                break
    if passed==0:
        return False
    #Check that the conf is in posotion to play any played note in the next period
    #Also check that any note ringed can ring in the next period
    if check_tp1:
        passed = 0
        for n in range(conf_list_tp1.shape[0]):
            if can_follow(conf, conf_list_tp1[n]):
                if (not must_change(conf, conf_list_tp1[n], ring_list_tp1[n])) and ring_can_stay(conf,ring,conf_list_tp1[n]):
                    passed = 1
                    break
        if passed==0:
            return False
    #Check that the conf are in position to play a string that will be played in the next period:

    return True

@njit
def _get_conf_ring_list(conf_list_tm1, ring_list_tm1, conf_list_t, ring_list_t,conf_list_tp1,ring_list_tp1, check_tp1):
    '''
    get_conf_ring_list(conf_list_tm1, ring_list_tm1, conf_list_t,notes).
    Takes a conf and ring list from t-1 and a potential lists of confs at t. Generates conf_ring_t
    '''
    valid_confs = []
    valid_rings = []
    for n in range(conf_list_t.shape[0]):
        if valid_conf_ring(conf_list_t[n],ring_list_t[n],conf_list_tm1,ring_list_tm1,conf_list_tp1,ring_list_tp1, check_tp1):
            valid_confs.append(conf_list_t[n])
            valid_rings.append(ring_list_t[n])
    return valid_confs, valid_rings

def get_conf_ring_list(conf_list_tm1, ring_list_tm1, conf_list_t, ring_list_t,conf_list_tp1,ring_list_tp1, check_tp1):
    '''
    get_conf_ring_list(conf_list_tm1, ring_list_tm1, conf_list_t,notes).
    Takes a conf and ring list from t-1 and a potential lists of confs at t. Generates conf_ring_t
    '''
    a, b = _get_conf_ring_list(conf_list_tm1, ring_list_tm1, conf_list_t, ring_list_t,conf_list_tp1,ring_list_tp1, check_tp1)
    return np.stack(a,dtype=np.int_), np.stack(b,dtype=np.int_)

#########################################################################
#Functions to write "sheet notes", i.e. suggested ways to play the notes#
#########################################################################

#Find all possible ways to play the notes:
@njit
def _append_to_sheets(conf_list_t,ring_list_t,conf_list_tm1,ring_list_tm1,sheets,pedal_changes_tm1):
    '''For each sheet music (configurations + ring) currently done at t-1, append sheet in t.'''
    new_sheets = []
    pedal_changes = []
    for idx_sheet in range(sheets.shape[0]):
        for idx_t in range(conf_list_t.shape[0]):
            idx_tm1 = sheets[idx_sheet][-1]
            #Check whether the configuration can follow any of the previous configurations, and that the pedal change does not affect any of the ringing notes from last period.
            if can_follow(conf_list_tm1[idx_tm1], conf_list_t[idx_t]) and does_not_affect_ringing(conf_list_t[idx_t], conf_list_tm1[idx_tm1], ring_list_tm1[idx_tm1]):
                #Check that ring does not play string currently being changed by pedal
                if does_not_play_changing(conf_list_t[idx_t],ring_list_t[idx_t],conf_list_tm1[idx_tm1]):
                    new_sheets.append(np.concatenate((sheets[idx_sheet],np.array([idx_t],dtype=np.int_))))
                    pedal_changes.append(np.sum(conf_list_tm1[idx_tm1]!=conf_list_t[idx_t])+pedal_changes_tm1[idx_sheet])
    return new_sheets, np.array(pedal_changes)

#for n_t in range(conf_list[0].shape[0])

def append_to_sheets(conf_list_t,ring_list_t,conf_list_tm1,ring_list_tm1,sheets,pedal_changes_tm1):
    '''For each sheet music (configurations + ring) currently done at t-1, append sheet in t.'''
    a, b = _append_to_sheets(conf_list_t,ring_list_t,conf_list_tm1,ring_list_tm1,sheets,pedal_changes_tm1)
    return np.stack(a), np.array(b)

@njit
def _append_to_sheets_loop(conf_lists,ring_lists,sheets,pedal_changes_tm1):
    new_sheets = []
    pedal_changes = []
    for idx_sheet in range(sheets.shape[0]):
        T = len(conf_lists)
        idx_tT = sheets[idx_sheet][-1]
        idx_t0 = sheets[idx_sheet][0]
        #Check whether the configuration in t=0 can follow the one on t=T, and that the pedal change does not affect any of the ringing notes from period T.
        if can_follow(conf_lists[T][idx_tT], conf_lists[0][idx_t0]) and does_not_affect_ringing(conf_lists[0][idx_t0], conf_lists[T][idx_tT], ring_lists[T][idx_tT]):
            #Check that ring does not play string currently being changed by pedal
            if does_not_play_changing(conf_lists[0][idx_t0],ring_lists[0][idx_t0],conf_lists[T][idx_tT]):
                new_sheets.append(sheets[idx_sheet])
                pedal_changes.append(np.sum(conf_lists[0][idx_t0]!=conf_lists[T][idx_tT])+pedal_changes_tm1[idx_sheet])
    return new_sheets, np.array(pedal_changes)

def append_to_sheets_loop(conf_list_t,ring_list_t,conf_list_tm1,ring_list_tm1,sheets,pedal_changes_tm1):
    a, b = _append_to_sheets(conf_list_t,ring_list_t,conf_list_tm1,ring_list_tm1,sheets,pedal_changes_tm1)
    return np.stack(a), np.array(b)
def get_min_sheet_locations(conf_lists,ring_lists,T, loop):
    sheets = np.arange(conf_lists[0].shape[0], dtype=np.int_)
    sheets = sheets.reshape((sheets.shape[0], 1))
    pedal_changes = np.zeros(sheets.shape[0])

    if T==1:
        sheets, pedal_changes = append_to_sheets(conf_lists[0], ring_lists[0], conf_lists[0], ring_lists[0],
                                                 sheets, pedal_changes)
        min_changes = np.where(pedal_changes == pedal_changes.min())[0]
    else:
        for t in range(1,T): #Don't need to check the first, it's already a list of valid configurations
            sheets, pedal_changes = append_to_sheets(conf_lists[t], ring_lists[t], conf_lists[t - 1], ring_lists[t - 1], sheets, pedal_changes)

        if loop:
            sheets, pedal_changes = append_to_sheets_loop(conf_lists[0], ring_lists[0], conf_lists[T - 1], ring_lists[T - 1], sheets, pedal_changes)

        min_changes = np.where(pedal_changes == pedal_changes.min())[0]

    return len(sheets), sheets[min_changes]


######################
#Combine into a class#
######################

def strarray(arr):
    string = '['
    for n in arr:
        s = str(n)
        if len(s)==1:
            s = '  '+s
        else:
            s = ' '+s
        string += s
    string += ']'
    return string

class Solver:
    def __init__(self, tune, T, loop):
        self.tune = tune
        self.T = T

        self.loop = loop
        self.conf_lists = [[] for _ in range(T)]
        self.ring_lists = [[] for _ in range(T)]

        # get all possible pedal configurations consistent with notes
        for t in range(T):
            self.conf_lists[t] = get_confs_from_notes(np.array(tune[t], dtype=np.int_))

        # Make lists of all pedal configurations and rings that plays the current notes:
        for t in range(T):
            self.conf_lists[t], self.ring_lists[t] = firstpass(self.conf_lists[t], np.array(tune[t], dtype=np.int_))

        self.best_sheets = []

        self.solve()

    def solve(self):
        n_configurations_tm1 = [3 ** 7 for a in self.conf_lists]
        n_configurations_t = [a.shape[0] for a in self.conf_lists]

        n_loops = 0

        t0 = 0 if self.loop else 1

        while n_configurations_tm1 != n_configurations_t:
            n_configurations_tm1 = n_configurations_t.copy()

            for t in range(t0,self.T):
                check_tp1 = False if not self.loop and t==self.T-1 else True
                tm1 = (t - 1) % self.T
                tp1 = (t + 1 ) % self.T
                self.conf_lists[t], self.ring_lists[t] = get_conf_ring_list(self.conf_lists[tm1],
                                                                            self.ring_lists[tm1],
                                                                            self.conf_lists[t], self.ring_lists[t],
                                                                            self.conf_lists[tp1],self.ring_lists[tp1],
                                                                            check_tp1)

            n_configurations_t = [a.shape[0] for a in self.conf_lists]
            #print(n_configurations_t)
            n_loops += 1

        #print(f'n_loops: {n_loops}')
    def permute_conf(self,perm): #Permutes the columns such that they are in actual harp pedal order, and adds one to be used as indices later.
        for t in range(self.T):
            #self.conf_lists[t] = self.conf_lists[t] #+1
            self.conf_lists[t] = self.conf_lists[t][:,perm] #+1

    def get_sheets(self, eng):
        tot_sheets, sheets = get_min_sheet_locations(self.conf_lists, self.ring_lists,self.T, self.loop)  # Find sheets with minimal number of pedal moves

        n_sheets = sheets.shape[0]
        if eng:
            string = f'Found {tot_sheets} possible way(s) to play the sequence. Showing {n_sheets} sequence(s) with the minimal number of pedal changes.'
            string += '\n\nNotation:\n - First line denotes note.\n - Second line denotes string.\n - Line 6-7 denotes pedal configurations.\n'
        else:
            string = f'Fant {tot_sheets} mulig(e) måter å spille sekvensen på. Viser {n_sheets} sekvense(r) som innebærer færrest endringer av pedalene.'
            string += '\n\nNotasjon:\n - Første linje angir tone.\n - Andre linje angir streng.\n - Linje 6-7 angir pedal-konfigurasjoner.\n'

        # Permute pedal configurations to pedal notation
        perm_to_pedal = [1, 0, 6, 2, 3, 4, 5]
        self.permute_conf(perm_to_pedal)
        n = 1
        for sheet in sheets:  # print sheets
            string += write_sheet(self.tune, self.conf_lists, self.ring_lists, sheet,n, eng)
            n += 1
        # permute pedal configurations to order C,D,E,F,G,A,B
        perm_inverse = [1, 0, 3, 4, 5, 6, 2]
        self.permute_conf(perm_inverse)

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
        return get_all_avail_notes(self.T, self.conf_lists,self.ring_lists, self.loop)
        #return self.get_avail_notes2()

    #Alternative way of getting available notes - by testing every non-used note from scratch. It's less bug prone, but really slow.
    #can also try to add the note to the current configuration, and only test that t.
    def get_avail_notes2(self):
        avail_notes = []
        for t in range(self.T):
            test_notes = set(range(12)) - set(self.tune[t])
            for note in test_notes:
                tune_copy = deepcopy(self.tune)
                if tune_copy[t][0]==12:
                    tune_copy[t]=[note]
                else:
                    tune_copy[t].append(note)
                tune_copy[t].append(note)
                try:
                    _ = Solver(tune_copy, self.T)
                    avail_notes.append(f'{note}_{t}')
                except ValueError as e:
                    pass
        return avail_notes

#Test
if __name__ == "__main__":
    tune = [[0],[5],[1],[6],[2],[7],[3],[8]]
    solver = Solver(tune,len(tune), True)
    print(solver.get_sheets(eng=False))