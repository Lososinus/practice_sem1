from loops import *

def main():            # в этой функции происходит инициализация и закрытие игры.
    game = Game_state()
    sandbox_loop(game, Game_state.FINISHED)
    game.quit()

if __name__ == "__main__":
    main()


