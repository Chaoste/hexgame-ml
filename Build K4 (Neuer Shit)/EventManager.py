class EventManager:
    
    Events = {}
    
    # add events users can listen to
    @staticmethod
    def registerEvent(event):
        EventManager.Events[event] = []
    
    # define all events
    @staticmethod
    def initEvents():
        
        EventManager.registerEvent("GameStarting")
        EventManager.registerEvent("GameStarted")
        
        EventManager.registerEvent("GameFinished")
        
        EventManager.registerEvent("MoveBegan")
        EventManager.registerEvent("MoveDenied")
        EventManager.registerEvent("MoveFinished")
        
        EventManager.registerEvent("PlayerChanged")
        
        EventManager.registerEvent("GameUILoaded")
        
        EventManager.registerEvent("UITick")
        
        EventManager.registerEvent("ToggleVictoryPath")
    
    # add subscriber to the specific events
    @staticmethod
    def subscribe(event, callback):
        EventManager.Events[event].append(callback)
    
    # called to notify all subscribers
    @staticmethod
    def notify(event):
        for func in EventManager.Events[event]:
            func()