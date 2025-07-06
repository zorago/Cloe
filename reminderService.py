import datetime as dt
import pickle
import customtkinter as ctk
from reminderModel import ReminderModel
from messageInterface import MessageInterface as message
from messageInterface import ValidationMessageInterface as validationMessage
from reminderInterface import ReminderInterface as reminderInterface
from apscheduler.schedulers.background import BackgroundScheduler


class ReminderService:

    reminders: dict[int, ReminderModel] = None
    scheduler = None
    root:ctk.CTk = None
    CurrentReminder = []
    parent = None

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.scheduler.add_job(self.cleanReminders, "interval", seconds=300)

        try:
            with open("data.pkl", "rb") as data:
                self.reminders = pickle.load(data)

            for key in self.reminders:
                if self.reminders[key]['_creationDate'] < dt.date.today() or self.reminders[key]['_remaining'] == 0:
                    self.delete(key)
                else:
                    print(key, '=>', self.reminders[key])
                    self.reminders[key]["_jobID"] = self.scheduler.add_job(self.temp, "interval", seconds=self.reminders[key]["_delay"], next_run_time=dt.datetime.combine(dt.datetime.today().date(), self.reminders[key]["startTime"]), args=[self.reminders[key]]).id

        except:
            message("Les datas n'ont pas pu être récupérées")

    def get(self):
        return self.reminders

    def save(self, name:str, startHour:str, startMinutes:str, endHour:str, endMinutes:str, count:str, measure:str, parent):

        if((type(name) != str) | (name == "")):
            message("Le nom est invalide")
            return
        
        for key in self.reminders:
            newName = self.reminders[key]['name']
            if newName == name:
                message("Un rappel de ce nom existe déjà")
                return
        
        try:
            startHour = int(startHour)
            startMinutes = int(startMinutes)
        except:
            message("L'heure de début est invalide")
            return


        try:
            endHour = int(endHour)
            endMinutes = int(endMinutes)
        except:
            message("L'heure de fin est invalide")
            return

        try:
            if(dt.time(startHour, startMinutes) >= dt.time(endHour, endMinutes)):
                message("L'heure de fin doit être ultérieure a l'heure de début")
                return
        except:
            message("Les valeurs rentrées ne correspondent pas au format d'une heure")
            return
        

        try:
            count = int(count)
        except:
            message("Le nombre de rappels demandé est invalide")
            return


        try:
            measure = int(measure)
        except:
            message("La quantité sélectionnée est invalide")
            return

        if((count < 1) | (measure < 1)):
            message("La valeur attendue doit être positive")
            return

        
        newId = self._generateId()
        newReminder:ReminderModel = {
            "id": newId,
            "name":name,
            "startTime":dt.time(startHour, startMinutes),
            "endTime":dt.time(endHour, endMinutes), 
            "count":count, 
            "measure":measure,
            "_remaining":count,
            "_currentMeasure":0,
            "_jobID":None,
            "_creationDate":dt.date.today()
        }

        newReminder["_delay"] = self._setDelay(newReminder["startTime"], newReminder["endTime"], newReminder["count"])
        self.reminders[newId] = newReminder
        self.parent.newTab(newId)
        

        with open("data.pkl", "wb") as data:
            pickle.dump(self.reminders, data)


        newReminder["_jobID"] = self.scheduler.add_job(self.temp, "interval", seconds=newReminder["_delay"], next_run_time=dt.datetime.combine(dt.datetime.today().date(), newReminder["startTime"]), args=[newReminder]).id

        validationMessage(f"Le rappel \"{name}\" a bien été créé :)", parent)


    
    def delete(self, reminderId:int):

        for key in self.reminders:

            if(key == reminderId):
                self.reminders.pop(key)
            
                with open("data.pkl", "wb") as data:
                    pickle.dump(self.reminders, data)

                return
    
    def temp(self, reminder):
        self.CurrentReminder.append(reminder)
        self.root.event_generate("<<OnReminder>>")

    def _generateId(self):
        ids = []
        for elem in self.reminders:
            ids.append(elem)

        ids.sort()

        if(len(ids) > 0):
            return ids.pop()+1
        return 1
            
    
    def validateReminder(self, reminder:ReminderModel, value:str):
        try:
            value = int(value)
            reminder["_currentMeasure"] += value
        except:
            message("La valeur rentrée doit être un chiffre entier")
            self.CurrentReminder.append(reminder)
            self.openReminder()


    def openReminder(self, *arg, **kwarg):
        reminder = self.CurrentReminder.pop()
        reminderInterface(reminder, self)
        
        remaining = reminder["_remaining"] - 1

        if (remaining == 0 ):
            try:
                self.scheduler.remove_job(reminder["_jobID"])
            except Exception as e:
                message("Echec de l'ouverture du rappel")
                print(e)
            try:
                id = None
                for key in self.reminders:
                    if key == reminder['id']:
                        id = key
                if id != None:
                    self.parent.deleteTab(id)
            except Exception as e:
                message("Echec de la suppression d'un rappel terminé !")
                print(e)

        
        else : 
            reminder["_remaining"] = remaining
        

    def _setDelay(self, start:dt.time, end:dt.time, count:int):
        startMin = (start.hour * 60 + start.minute) *60
        endMin = (end.hour * 60 + end.minute) *60

        return ((endMin-startMin)//count)+1
    
    def cleanReminders(self):
        if dt.time(0,0,0) < dt.datetime.now().time() < dt.time(0,6,0):
            for key in self.reminders:
                    if self.reminders[key]['_creationDate'] < dt.date.today() or self.reminders[key]['_remaining'] == 0:
                        self.scheduler.remove_job(self.reminders[key]["_jobID"])
                        self.delete(key)

