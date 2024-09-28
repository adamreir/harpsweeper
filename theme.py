################################################################################################
# The Layout class keeps track of the layout and some colors used manually as part of the layout#
################################################################################################


class Theme:
    """Class that defines and changes between the two PySimpleGui themes accessible in Harpsweeper.

     Also keeps track of a few manually defined colors, and the option that toggles a separate color for ringing notes.
     """
    def __init__(self, sg):
        sg.LOOK_AND_FEEL_TABLE['darkmode'] = {
            'BACKGROUND': '#121212',
            'TEXT': '#d8d8d8',
            'INPUT': '#212121',
            'SCROLL': '#E3E3E3',
            'TEXT_INPUT': '#d8d8d8',
            'BUTTON': ('#e9e9e9', '#1F1F1F'),
            'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
            'BORDER': 1,
            'SLIDER_DEPTH': 0,
            'PROGRESS_DEPTH': 0}
        sg.LOOK_AND_FEEL_TABLE['lightmode'] = {
            "BACKGROUND": "#e7e7e7",
            "TEXT": "#000000",
            "INPUT": "#ffffff",
            "TEXT_INPUT": "#000000",
            "SCROLL": "#1b6497",
            "BUTTON": ("#000000", "#fcfcfc"),
            "PROGRESS": sg.DEFAULT_PROGRESS_BAR_COMPUTE,
            "BORDER": 1,
            "SLIDER_DEPTH": 0,
            "PROGRESS_DEPTH": 0,
        }

        self.darkmode = True
        sg.theme('darkmode')

        self.show_ring_colors = True
        self.normal_button_font = ('helvetica', 11, 'bold')
        self.notebutton_active = '#33b249'
        self.notebutton_ring = '#229f8c'
        self.notebutton_avail = '#0B76BE'
        self.notebutton_disable = '#D61F2C'

    def update_theme(self, sg):
        if self.darkmode:
            sg.theme('darkmode')
        else:
            sg.theme('lightmode')

    @property
    def sbar_background_color(self):
        if self.darkmode:
            return '#686868'
        else:
            return '#CDCDCD'

    @property
    def sbar_trough_color(self):
        if self.darkmode:
            return '#424242'
        else:
            return '#F0F0F0'  # '#CDCDCD'

    @property
    def ring_color(self):
        if self.show_ring_colors:
            return self.notebutton_ring
        else:
            return self.notebutton_avail
