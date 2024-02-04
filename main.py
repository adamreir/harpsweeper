
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

    #Main loop
    goto = 'welcome'
    while goto != 'exit':
        match goto:
            case 'welcome':
                goto = welcome_screen(tune_holder, solver_holder, texts, theme)
            case 'about':
                goto = about_screen(texts)
            case 'license':
                goto = license_screen(texts)
            case 'main':
                goto = main_screen(tune_holder, solver_holder, texts, theme)
            case 'save':
                goto = save_load_screen(tune_holder, solver_holder, texts)