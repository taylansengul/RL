import states


class StateManager(object):
    def __init__(self):
        self.initializingState = states.InitialingState()
        self.mainMenuState = states.MainMenuState()
        self.mapState = states.MapState()
        self.quittingState = states.QuitingState()
        self.inventoryState = states.InventoryState()
        self.currentState = None

    def changeState(self, newState, sys):
        self.currentState = newState
        self.currentState.init(sys)