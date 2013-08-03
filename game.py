from system import System


class Game(object):
    def __init__(self):
        self.sys = System()

    def loop(self):
        self.sys.stateManager.changeState(self.sys.stateManager.initializingState, self.sys)
        self.sys.stateManager.changeState(self.sys.stateManager.mainMenuState, self.sys)
        while not self.sys.stateManager.currentState == self.sys.stateManager.quittingState:
            # get input
            self.sys.io_handler.compute_active_event(self.sys)
            # if there is input
            if self.sys.io_handler.active_event:
                # determine action
                self.sys.stateManager.currentState.determineAction(self.sys, self.sys.io_handler.get_active_event())
                # update graphics
                self.sys.graphics_engine.update_screen(self.sys)


def main():
    game = Game()
    game.loop()

if __name__ == '__main__':
    main()
