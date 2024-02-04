
import numpy as np

# Maps notes notated using integers to note names
note_map = {
    0: "C ",
    1: "Db",
    2: "D ",
    3: "Eb",
    4: "E ",
    5: "F ",
    6: "Gb",
    7: "G ",
    8: "Ab",
    9: "A ",
    10: "Bb",
    11: "B ",
    12: "- "
}

def repr_notes(notes, note_map):
    '''takes a set of notes in integer notation, and displays a sorted list of note names'''
    notes = notes.copy()
    for note_int in note_map:
        if note_int in notes:
            notes.remove(note_int)
            notes.add(note_map[note_int])

    # Sort
    note_order = {v: k for k, v in note_map.items()}
    notes = list(notes)
    notes.sort(key=lambda x: note_order[x])
    return notes

###############################
#Write sheet music in txt file#
###############################

map_string_name = {
    0:'C ',
    1:'D ',
    2:'E ',
    3:'F ',
    4:'G ',
    5:'A ',
    6:'B '
}

def _add_space(string,width,sep):
    space_before = max(0,int((width-len(string))/2))
    space_after  = max(0,int((width-len(string))/2+.5))
    return sep*space_before + string + sep*space_after

def add_space(note_string, ring_string, pedal_strings):
    width = max(len(note_string) + 2, len(ring_string) + 2, 21)

    note_string = _add_space(note_string, width, ' ')
    ring_string = _add_space(ring_string, width, ' ')

    pedal_strings[0] = _add_space(pedal_strings[0], width, '-')
    for n in range(1,5):
        pedal_strings[n] = _add_space(pedal_strings[n], width, ' ')

    return note_string, ring_string, pedal_strings


def write_bar(notes, conf, ring, rows, write_pedals):  #
    note_order = {v: k for k, v in note_map.items()}
    note_list = [note_map[a] for a in notes]
    note_list.sort(key=lambda x: note_order[x])
    note_string = ','.join(note_list)

    #Make ring string, but sort C and B according to the configuration to align with notes.
    ring_list = [map_string_name[a] for a in np.where(ring == 1)[0]]
    c_loc, b_loc = (1,2) #D, C, B | E, F, G, A
    if conf[c_loc]==-1 and conf[b_loc]!=1:
        ring_order = ['D ','E ','F ','G ','A ','B ','C ']
    elif conf[c_loc] != -1 and conf[b_loc] == 1:
        ring_order = ['B ','C ','D ', 'E ', 'F ', 'G ', 'A ']
    elif conf[c_loc] == -1 and conf[b_loc] == 1:
        ring_order = ['B ', 'D ', 'E ', 'F ', 'G ', 'A ','C ']
    else:
        ring_order = ['C ','D ','E ','F ','G ','A ','B ']
    ring_order = {ring_order[n]: n for n in range(7)}
    ring_list.sort(key=lambda x: ring_order[x])
    ring_string = ','.join(ring_list)

    pedal_strings = [' ' * 21 for _ in range(5)]
    pedal_strings[0] = '-'*21
    if write_pedals:
        pedal_strings[1] = ' '+ ' '.join(['D ', 'C ', 'B ','E ', 'F ', 'G ', 'A '])
        n = 1
        for configuration in conf: #Each configuration indicates a row with indices -1,0 and 1. Add three to access strings 2,3,4 (idx 0 and taken by hbar and pedal note row)
                pedal_strings[configuration+3] = pedal_strings[configuration+3][:n] + '|' + pedal_strings[configuration+3][n + 1:]
                n += 3
    note_string, ring_string, pedal_strings = add_space(note_string, ring_string, pedal_strings)
    rows[0].append(note_string)
    rows[1].append(ring_string)
    rows[2].append(pedal_strings[0])
    rows[3].append(pedal_strings[1])
    rows[4].append(pedal_strings[2])
    rows[5].append(pedal_strings[3])
    rows[6].append(pedal_strings[4])
    return rows

def write_sheet(tune,conf_lists,ring_lists,sheet,sheet_num,eng):
    rows = [[] for _ in range(7)]
    conf_tm1 = np.array([2, 2, 2, 2, 2, 2, 2], dtype=np.int_)
    for t in range(len(tune)):
        if np.array_equal(conf_lists[t][sheet[t]], conf_tm1):
            write_pedals = False
        else:
            write_pedals = True
        rows = write_bar(tune[t],conf_lists[t][sheet[t]],ring_lists[t][sheet[t]],rows,write_pedals)
        conf_tm1 = conf_lists[t][sheet[t]].copy()
    string = rows_to_string(rows,sheet_num, eng)
    return string

def rows_to_string(rows,sheet_num, eng):
    new_lsts=[[] for _ in range(7)]
    m=0
    for row in rows:
        n=0
        while n<=len(row)-1:
            new_lsts[m].append('%'.join(row[n:min(len(row),n+5)]))
            n+=5
        m+=1
    string = '\n\n' + '-'*(len(new_lsts[0][0])+2)
    if eng:
        string += f'\nSheet {sheet_num}:\n\n%'
    else:
        string += f'\nNote {sheet_num}:\n\n%'
    for n in range(len(new_lsts[0])):
        for m in range(7):
            string+=new_lsts[m][n] + '%\n%'
        string = string[0:len(string)-2]
        string += '\n\n\n%'
    string = string[0:len(string)-4]
    return string

######################################
#Write tune as a string for log-files#
######################################

def tune_as_string(tune):
    tune_string = '['
    n=0
    for bar in tune:
        if n==0:
            tune_string += '['
        else:
            tune_string += ', ['
        m=0
        for note in bar:
            if m==0:
                tune_string+=note_map[note]
            else:
                tune_string+=', ' + note_map[note]
            m+=1
        tune_string +=']'
        n+=1
    tune_string +=']'
    return tune_string
