#################################################################################
#The Texts class holds texts, and takes care of language and selected note order#
#################################################################################

class Texts:
    def __init__(self):
        self.eng = False
        #self.notelist = ['Bb','B','C','Db','D','Eb','E','F','Gb','G','Ab','A']
        #D, C, B | E, F, G, A
        self.notelist =    ['C', 'Cb', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self.pedal_order_no = ['V.',' ','V.',' ','H.','H.', ' ', 'H.', ' ', 'H.',' ','V.']
        self.pedal_order_en = ['L.', ' ', 'L.', ' ', 'R.', 'R.', ' ', 'R.', ' ', 'R.', ' ', 'L.']
        self.lastnote = 0
        self.reverse=True
        self.note_to_noteint = {self.notelist[a]:a for a in range(12)}
        self.noteint_to_note = {a:self.notelist[a] for a in range(12)}
        self.default_input = ''
    @property
    def ordered_notes(self):

        if self.reverse:
            order = [a % 12 for a in range(self.lastnote+11, self.lastnote-1,-1)]
        else:
            order = [a % 12 for a in range(self.lastnote - 11, self.lastnote+1)]

        if self.eng:
            pedal_order = self.pedal_order_en
        else:
            pedal_order = self.pedal_order_no

        notelist = [self.notelist[a] for a in order]
        pedal_order = [pedal_order[a] for a in order]
        noteint = [list(range(12))[a] for a in order]

        return pedal_order, notelist, noteint

    @property
    def bottom_note_str(self):
        return self.noteint_to_note[self.lastnote]

    @property
    def loop_checkmark_text(self):
        if self.eng:
            return 'Loop sequence'
        else:
            return 'Loop sekvensen'

    @property
    def bottom_note_checkmark_text(self):
        if self.eng:
            return 'Place note at bottom:'
        else:
            return 'Nederste note:'

    @property
    def reverse_text(self):
        if self.eng:
            return 'Reverse note order'
        else:
            return 'Inverter rekkefølgen'

    @property
    def notes(self):
        return self.notelist

    @property
    def welcome(self):
        if self.eng:
            desc_text = 'Welcome to Harpsweeper!'
            desc_text += '\n\nThis program aids composing and organizing sequences of notes for the harp.'
            desc_text += '\n\nHarpsweeper lets you generate a sequency of notes. It then shows the notes that can be added, given that'
            desc_text += '\n    - there exists a sequence of pedal configurations that can play the sequence.'
            desc_text += '\n    - only one pedal per foot can change in a single period.'
            desc_text += "\n    - pedals do not change at the same time or right after the corresponding string is played."
            desc_text += '\n\nNote that Harpsweeper'
            desc_text += '\n    - abstracts away from strings. I.e. Ab represents both Ab and G#.'
            desc_text += '\n    - can suggested pedal sequences for the selected notes.'
            desc_text += '\n    - does not take hand position or fingering reach into account.'
            desc_text += '\n\nShort user guide for the main screen:'
            desc_text += '\n   - Each column represents one period (e.g. one quarter note).'
            desc_text += '\n   - Blue buttons represents available tones.'
            desc_text += '\n   - Green buttons represents selected tones.'
            desc_text += '\n   - Turquoise buttons are notes ringing from the previous period.'
            desc_text += '\n   - Red buttons are tones that are not possible to play, given selected notes and the restrictions above.'
            desc_text += '''\n   - Enable the 'loop'-option if the first period is also played after the last.'''
            desc_text += '\n\n Select number of periods, or load an existing sequence: '
        else:
            desc_text = 'Velkommen til Harpsweeper!'
            desc_text += '\n\nDette programmet er skrevet for å støtte komponering og organisering for harpe.'
            desc_text += '\n\nHarpsweeper lar deg generere en rekke av toner, og viser hvilke toner som kan legges til ved å sjekke'
            desc_text += '\n    - at det finnes en sekvens av pedalkonfigurasjoner som kan spille valgte toner.'
            desc_text += '\n    - at at ikke mer enn én pedal per fot endres per periode.'
            desc_text += '\n    - at en pedal ikke endres samtidig eller rett etter at tilhørende streng spilles.'
            desc_text += '\n\nMerk at Harpsweeper'
            desc_text += '\n    - Fokuserer på toner. Dvs. at Ab representerer både Ab og G#.'
            desc_text += '\n    - kan vise forslag til pedalkonfigurasjoner for å spille valgte toner.'
            desc_text += '\n    - ikke tar hensyn til hånd- eller fingerstilling.'
            desc_text += '\n\nKort brukerveiledning til hovedskjermen:'
            desc_text += '\n    - Hver kolonne representerer én periode (f.eks. en kvartnote).'
            desc_text += '\n    - Blå knapper representerer toner som kan legges til.'
            desc_text += '\n    - Grønne knapper representerer valgte toner.'
            desc_text += '\n    - Turkise knapper representerer toner som fremdeles ringer etter forrige periode.'
            desc_text += '\n    - Røde knapper er toner som det er ikke mulig å spille, gitt valgte toner og reglene over.'
            desc_text += '''\n   - Bruk 'loop' dersom den første perioden også skal spilles etter den siste.'''
            desc_text += '\n\n Velg antall perioder, eller åpne en eksisterende sekvens: '
        return desc_text

    @property
    def about(self):
        if self.eng:
            return ['This program is developed by Adam Reiremo.',
                    '''Please do not hesitate to send me email at''',
                    'if you have any questions or requests.',
                    'The source code for Harpsweeper is available at']
        else:
            return ['Dette programmet er utviklet av Adam Reiremo.',
                    'Vennligst send en epost til',
                    'hvis du har noen spørsmål eller forespørsler.',
                    'Kildekoden for Harpsweeper er tilgjengelig på']

    @property
    def license_button(self):
        if self.eng:
            return 'Open license'
        else:
            return "Åpen lisens"
    @property
    def send_email(self):
        if self.eng:
            return 'Send email'
        else:
            return 'Send epost'

    @property
    def about_button(self):
        if self.eng:
            return 'About'
        else:
            return 'Om programmet'

    @property
    def open(self):
        if self.eng:
            return 'Open a sequence'
        else:
            return 'Åpne en seksens'

    @property
    def select_periods(self):
        if self.eng:
            return 'You have to select number of periods.'
        else:
            return 'Du må velge antall perioder.'

    @property
    def only_numbers(self):
        if self.eng:
            return 'Only numbers are allowed.'
        else:
            return 'Kun tall er tillatt.'

    @property
    def harpsweeper_files(self):
        if self.eng:
            return 'Files that can be used by Harpsweeper:'
        else:
            return 'Filer som kan leses av dette programmet:'
    @property
    def cannot_load(self):
        if self.eng:
            return 'Unable to load file.'
        else:
            return 'Kunne ikke laste filen.'

    @property
    def not_with_loop(self):
        if self.eng:
            return 'Cannot play this sequence in a loop.'
        else:
            return 'Kan ikke spille denne sekvensen i loop.'

    @property
    def save(self):
        if self.eng:
            return 'Save sequence'
        else:
            return 'Lagre sekvens'

    @property
    def darkmode(self):
        if self.eng:
            return 'Dark mode'
        else:
            return 'Mørk bakgrunn'

    @property
    def export(self):
        if self.eng:
            return 'Export sequence to text file (with pedal suggestions):'
        else:
            return 'Eksporter noter til tekstfil (med pedalsekvenser):'

    @property
    def export_button(self):
        if self.eng:
            return 'Export'
        else:
            return 'Eksporter'
    @property
    def back(self):
        if self.eng:
            return 'Back'
        else:
            return 'Tilbake'
    @property
    def restart(self):
        if self.eng:
            return 'Start over'
        else:
            return 'Start på nytt'

    @property
    def save_or_load(self):
        if self.eng:
            return 'Save, open or export a sequence'
        else:
            return 'Lagre, åpne eller eksporter en sekvens'

    def license(self, get_filename):
        with open(get_filename('LICENSE'), 'r') as f:
            license_text = f.read()
        return license_text
