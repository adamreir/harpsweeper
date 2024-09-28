
#Import from harpsweeper files:
from texts import Texts
from theme import Theme
from layouts import *
from holders import TuneHolder, SolverHolder

if __name__ == '__main__':
    solver_holder = SolverHolder()
    tune_holder = TuneHolder()
    texts = Texts()
    theme = Theme(sg)

    #Main loop. goto decides which page to open next
    goto = 'welcome'
    while goto != 'exit':
        match goto:
            case 'welcome':
                goto = show_welcome_page(tune_holder, solver_holder, texts, theme)
            case 'about':
                goto = show_about_page(texts)
            case 'license':
                goto = show_license_page(texts)
            case 'main':
                goto = show_main_page(tune_holder, solver_holder, texts, theme)
            case 'save':
                goto = show_save_load_page(tune_holder, solver_holder, texts)