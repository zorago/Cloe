import datetime as dt

class ReminderModel:
    name:str = None
    startTime:dt.time = None
    endTime:dt.time = None
    count:int = None
    measure:int = None
    _delay:int = None #Tous les combiens la notif doit être envoyée : ratio deltaTime et count
    _remaining:int = None # Count -- par notif envoyée
    _currentMeasure:int = None # Total des mesures entrées par l'utilisateur
        