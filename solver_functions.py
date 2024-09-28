from numba import njit
import numpy as np


########################################################
# Find possible configurations and corresponding rings #
########################################################
@njit(cache=True)
def can_follow(a, b):
    """
    Checks whether configuration b can follow configuration a.
    Returns True if each foot changes only one pedal between the configurations"""
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


@njit(cache=True)
def possible_strings(conf, note):
    """
    Documents all the possible ways a configuration can play a note (1 or 2 ways if possible).
    I.e. which strings gives the required note."""
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
    """Returns ways to play notes, given a pedal configuration."""
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
    return old_rings


@njit(cache=True)
def get_avail_notes_from_conf(conf, avail_strings):
    """
    Transforms a configuration to a list of available notes.
    Returns a list of notes, indexed by the corresponding string. Unavailable strings have value -1"""
    notes = np.array([-1, -1, -1, -1, -1, -1, -1], dtype=np.int_)
    for n in range(7):
        if avail_strings[n] == 1:
            if n < 3:
                notes[n] = (2*n + conf[n]) % 12
            else:
                notes[n] = (2*n - 1 + conf[n]) % 12
    return notes


@njit
def get_avail_strings(conf_t, conf_list_tm1, ring_list_tm1):
    """
    Returns a list of available strings,
    given a pedal configuration and all configuration * corresponding rings from period t-1"""
    avail_strings = np.array([0,0,0,0,0,0,0], dtype=np.int_)
    all_strings_avail = np.array([1,1,1,1,1,1,1])
    for idx_tm1 in range(conf_list_tm1.shape[0]):
        if can_follow(conf_t,conf_list_tm1[idx_tm1]) and does_not_affect_ringing(conf_t, conf_list_tm1[idx_tm1], ring_list_tm1[idx_tm1]):
            for n in range(7):
                ring_t = np.array([0,0,0,0,0,0,0], dtype=np.int_)
                ring_t[n]=1
                if does_not_play_changing(conf_t, ring_t, conf_list_tm1[idx_tm1]):
                    if conf_t[n]==conf_list_tm1[idx_tm1][n]:
                        avail_strings[n]=1
        if np.array_equal(avail_strings,all_strings_avail):
            return avail_strings
    return avail_strings


@njit
def get_avail_strings_tp1(conf,conf_list_tp1):
    """
    Checks if each string can be played.
    False (returned as 0) if the string have to change in the next period. I.e. the string is not allowed to ring."""
    arr = np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.int_)
    for conf_tp1 in conf_list_tp1:
        for n in range(7):
            if conf[n] == conf_tp1[n] and can_follow(conf, conf_tp1):
                arr[n] = 1
    return arr


@njit
def _get_all_avail_notes(conf_list_t, conf_list_tm1, ring_list_tm1, conf_list_tp1, check_tm1, check_tp1):
    """Returns a list of all available notes, formatted as a boolean array"""
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
        for note in get_avail_notes_from_conf(conf,avail_strings):
            if note != -1:
                avail_notes[note] = 1
        if np.array_equal(avail_notes, all_notes_avail):
            return avail_notes
    return avail_notes


def get_all_avail_notes(T, conf_lists,ring_lists, loop):
    """Returns a list of all available notes, formatted as a boolean array"""
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
    """Generates the full list of 7^3 possible pedal configurations in a single period."""
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
    """
    Checks which notes are available from a pedal configuration.
    Returns an array of notes, where the index indicates string."""
    notes = np.empty(7, dtype=np.int_)
    for n in range(7):
        if n<3:
            notes[n] = (2*n + conf[n]) % 12
        else:
            notes[n] = (2*n -1 + conf[n]) % 12
    return notes


@njit(cache=True)
def _get_confs_from_notes(notes: list[int]):
    """Generate a list of all configurations that can play the selected notes."""
    all_confs = []

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
    if notes[0] == 12: #12 means that no notes are selected, i.e. all configurations are valid.
        conf_list = gen_all_possible_confs()
    else:
        conf_list = np.stack(_get_confs_from_notes(notes), dtype=np.int_)
    return np.stack(conf_list, dtype=np.int_)


@njit(cache=True)
def _firstpass(conf_list, notes):
    '''Takes a list of pedal configurations and notes, and returns lists of all combinations of confs and rings that will play the notes'''
    new_confs = []
    new_rings = []
    for conf in conf_list:
        rings = ring_from_notes_conf(conf, notes)
        for ring in rings:
            new_confs.append(conf)
            new_rings.append(ring)
    return new_confs, new_rings


def firstpass(conf_list, notes):
    '''Wrapper for _firstpass'''
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
    '''
    Checks that ring_t does not try to play a string that is changing pitch.
    Does the same as does_not_affect_ringing. Duplicated for clarification through function names.
    '''
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
    # Check that the conf is in position to play any string played in the next period.
    # Also check that any note plucked can ring in the next period.
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


# Unused functions:
# def possible_conf2(conf1, conf2):
#     '''Removes configurations in conf2 that cannot follow any of the configurations in conf1'''
#
#     new_conf2 = []
#     for n in range(len(conf2)):
#         for m in range(len(conf1)):
#             if can_follow(conf2[n], conf1[m]):
#                 new_conf2.append(conf2[n])
#                 break
#
#     return new_conf2
#
#
# def conf_can_play(conf, notes):
#     '''Checks if pedal configuration can play the set (list) of notes'''
#     avail_notes = get_avail_notes(conf)
#     for note in notes:
#         if note not in avail_notes:
#             return False
#     return True