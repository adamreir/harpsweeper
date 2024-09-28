
from numba import njit
import numpy as np
from solver_functions import can_follow, does_not_affect_ringing, does_not_play_changing

############################################################################
# Functions that finds all possible "sheets", and extracts the sheets with #
# the lowest number of pedal changes                                       #
############################################################################

# Find all possible ways to play the notes (i.e. all sheets):


@njit
def _append_to_sheets(conf_list_t,ring_list_t,conf_list_tm1,ring_list_tm1,sheets,pedal_changes_tm1):
    """Combines sheet music currently stopping at t-1 with configurations from t.
    Constructs a new list of sheets stopping at t.
    Note that the list of sheets can grow.
    """
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


def append_to_sheets(conf_list_t,ring_list_t,conf_list_tm1,ring_list_tm1,sheets,pedal_changes_tm1):
    """Combines sheet music currently complete at t-1 with configurations from t.
    Constructs a new list of sheets complete at t.
    Note that the list of sheets can grow.
    This function is a wrapper for the njit decorated function _append_to_sheets()"""
    a, b = _append_to_sheets(conf_list_t,ring_list_t,conf_list_tm1,ring_list_tm1,sheets,pedal_changes_tm1)
    return np.stack(a), np.array(b)

@njit
def _remove_non_loopable_sheets(pedal_list_0, ring_list_0, pedal_list_T, ring_list_T, T, sheets, pedal_changes):
    """Removes sheet music that is not loopable.
    The list of sheets might shrink, but not grow."""
    new_sheets = []
    new_pedal_changes = []
    #for idx_sheet in range(sheets.shape[0]):
    for idx in range(sheets.shape[0]):
        sheet = sheets[idx]
        pedal_change = pedal_changes[idx]

        pedalT = pedal_list_T[sheet[T-1]]
        pedal0 = pedal_list_0[sheet[0]]
        ringT = ring_list_T[sheet[T - 1]]
        ring0 = ring_list_0[sheet[0]]

        print('check 0:')
        print('   pedal:')
        print(pedal0)
        print('   ring:')
        print(ring0)
        print('check T:')
        print('   pedal:')
        print(pedalT)
        print('   ring:')
        print(ringT)
        passed = False
        print('')
        #Check whether the configuration can follow any of the previous configurations, and that the pedal change does not affect any of the ringing notes from last period.
        if can_follow(pedalT, pedal0) and does_not_affect_ringing(pedal0, pedalT, ringT):
            #Check that ring does not play string currently being changed by pedal
            if does_not_play_changing(pedal0, ring0, pedalT):
                print('passed')
                passed = True
                new_sheets.append(sheet)
                new_pedal_changes.append(pedal_change)

        if not passed:
            print('failed')
        print('')
    return new_sheets, new_pedal_changes


def remove_non_loopable_sheets(pedal_list_0, ring_list_0, pedal_list_T, ring_list_T, T, sheets, pedal_changes):
    a, b = _remove_non_loopable_sheets(pedal_list_0, ring_list_0, pedal_list_T, ring_list_T, T, sheets, pedal_changes)
    return np.stack(a), np.array(b)
def find_sheets(pedal_lists, ring_lists, T, loop):
    """
    Takes the list of pedal configurations and corresponding string plucks.
    Returns sheet music formatted as numpy Arrays"""
    sheets = np.arange(pedal_lists[0].shape[0], dtype=np.int_)
    sheets = sheets.reshape((sheets.shape[0], 1))
    pedal_changes = np.zeros(sheets.shape[0])

    if T==1: # Should treat loop==True and loop=False as separate cases, but T==1 is the trivial case.
        sheets, pedal_changes = append_to_sheets(
            pedal_lists[0],
            ring_lists[0],
            pedal_lists[0],
            ring_lists[0],
            sheets,
            pedal_changes
        )
        min_changes = np.where(pedal_changes == pedal_changes.min())[0]
    else:
        for t in range(1, T):  # Don't need to check the first (index 0), it's already a valid list of sheets stopping in period 0
            sheets, pedal_changes = append_to_sheets(
                pedal_lists[t],
                ring_lists[t],
                pedal_lists[t - 1],
                ring_lists[t - 1],
                sheets,
                pedal_changes
            )

        if loop:
            sheets, pedal_changes = remove_non_loopable_sheets(pedal_lists[0],
                                                               ring_lists[0],
                                                               pedal_lists[T-1],
                                                               ring_lists[T-1],
                                                               T,
                                                               sheets,
                                                               pedal_changes
                                                               )

        min_changes = np.where(pedal_changes == pedal_changes.min())[0]

    return len(sheets), sheets[min_changes]

