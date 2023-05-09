from uasyncio import Event


class GlobalState:
    def __init__(self):
        self.state = {}
        self.stateChangedEvent = Event()

    def setState(self, key, value):
        self.state[key] = value

    def getState(self, key=None):
        if key is None:
            return self.state
        return self.state.get(key)

    def addState(self, new_state):
        if isinstance(new_state, dict):
            self.state.update(new_state)
        else:
            raise ValueError("The 'new_state' argument must be a dictionary.")

    def setCurrentProfile(self, profileNr):
        self.setState("current_profile", profileNr)
        self.stateChangedEvent.set()

    async def awaitStateChange(self):
        await self.stateChangedEvent.wait()
        self.stateChangedEvent.clear()


state = GlobalState()
