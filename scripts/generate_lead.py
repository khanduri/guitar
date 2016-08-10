import sys
import copy
from os import walk


TABS = {
    'E': 0,
    'B': 1,
    'G': 2,
    'D': 3,
    'A': 4,
    'e': 5,
}
LEAD_TEMPLATE = [
    ['E'],
    ['B'],
    ['G'],
    ['D'],
    ['A'],
    ['e'],
]
SONG_LEAD_TEMPLATE = [[],[],[],[],[],[],]


songs_folder = sys.argv[1]
leads_folder = 'leads'


def clean_file(file_to_open):
    for line in open(file_to_open):
        if line.startswith('//') or not line.strip():
            continue

        no_space_line = line.strip()
        yield no_space_line


def print_lead(lead):
    if type(lead) == str:
        file_to_write.write(lead.strip())
    else:
        for tabs,template in zip(lead, LEAD_TEMPLATE):
            file_to_write.write('{0}:{1}'.format(template[0], ''.join(tabs)))
            file_to_write.write('\n')
    file_to_write.write('\n\n')


def add_song_lead(song_lead, notes):
    note_map = {TABS[n[0]]: n[1:] for n in notes}
    for index in xrange(len(LEAD_TEMPLATE)):
        if index in note_map.keys():
            song_lead[index].append('{0:->2} '.format(note_map[index]))
        else:
            song_lead[index].append('-- ')


def fetch_song_files():
    song_files = []
    for (dirpath, dirnames, filenames) in walk(songs_folder):
        song_files.extend(filenames)
        break
    return song_files


def generate_song_lead(line):
    chunks = line.split()
    song_lead = copy.deepcopy(SONG_LEAD_TEMPLATE)
    for chunk in chunks:
        notes = chunk.split('-')

        operators = {n[0]: n[1:] for n in notes}

        if len(operators) == 1:
            operator = operators.keys()[0]
            if operator not in TABS:
                # if operator == '*':
                #     count = int(operators.values()[0])
                #     for _ in xrange(count):
                #         song_lead = copy.deepcopy(song_lead)
                #         song_leads.append(song_lead)
                #     song_lead = copy.deepcopy(SONG_LEAD_TEMPLATE)
                if operator == '.':
                    for index in xrange(len(LEAD_TEMPLATE)):
                        song_lead[index].append('. ')
            else:
                add_song_lead(song_lead, notes)

        elif len(operators) > 1:
            add_song_lead(song_lead, notes)
        else:
            print 'Corrupt line: {0}'.format(line)

    return song_lead



for song_file in fetch_song_files():
    file_to_open = "/".join([songs_folder, song_file])
    file_to_write = open("/".join([leads_folder, song_file]), 'w')
    
    song_leads = []
    for line in clean_file(file_to_open):

        if line.startswith('#'):
            # this is the song lyrics
            song_leads.append(line)
            continue

        song_lead = generate_song_lead(line)

        if song_lead != SONG_LEAD_TEMPLATE:
            song_leads.append(song_lead)

    for lead in song_leads:
        print_lead(lead)
