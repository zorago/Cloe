import sys
import customtkinter as ctk
from geometryCalcutator import set
from colors import Colors
from reminderService import ReminderService
from newReminder import NewReminder
from reminderInterface import ReminderInterface as reminderInterface


class ResumeInterface:

    service = None
    root = None
    newReminderWindow = None

    def __init__(self): 

        self.root =ctk.CTk()
        self.service = ReminderService()
        self.service.root = self.root
        self.service.parent = self
        self.open()
        

    def open(self):
        # Window
        self.root.title("rememberMe")
        self.root.geometry(set(370, 400))
        self.root.resizable(False,False)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=2)
        self.root.grid_columnconfigure(0, weight=1)

        # Title
        headFrame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        headFrame.grid(row=0, sticky="ns", pady=(12,0))
        headFrame.grid_rowconfigure(0, weight=1)

        headTitle = ctk.CTkLabel(master=headFrame, text="rememberMe", font=ctk.CTkFont(size=24, weight="bold"))
        headTitle.grid(row=0, column=0, padx=(70,0))

        addBtn = ctk.CTkButton(master=headFrame, text="+", fg_color=Colors.darkBtnColor, hover_color=Colors.hghColor, width=30, command=self.openNewReminder)
        addBtn.grid(row=0, column=1, padx=(48,0))

        #Resume
        self.resumeTab = ctk.CTkTabview(master=self.root, height=300, segmented_button_selected_color=Colors.btnColor, segmented_button_selected_hover_color=Colors.hghColor)
        self.resumeTab.grid(row=1)
        self.resumeTab.grid_columnconfigure(0, weight=1)

        for key in self.service.reminders:
            self.newTab(key)

        self.root.bind("<<OnReminder>>", self.service.openReminder)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()
        
    def newTab(self, key):
        self.resumeTab.add(self.service.reminders[key]['name'])

        startTitle=ctk.CTkLabel(master=self.resumeTab.tab(self.service.reminders[key]['name']), 
                                text=f"A commencé à {self.service.reminders[key]['startTime'].strftime("%H")} h {self.service.reminders[key]['startTime'].strftime("%M")}")
        startTitle.grid(row=1, sticky="w", padx=(24,0), pady=(24,0))

        endTitle=ctk.CTkLabel(master=self.resumeTab.tab(self.service.reminders[key]['name']), 
                            text=f"Se termine à {self.service.reminders[key]['endTime'].strftime("%H")} h {self.service.reminders[key]['endTime'].strftime("%M")}")
        endTitle.grid(row=2, sticky="w", padx=(24,0))

        countTitle=ctk.CTkLabel(master=self.resumeTab.tab(self.service.reminders[key]['name']), text=f"Nombre de rappel à venir : {self.service.reminders[key]['_remaining']}")
        countTitle.grid(row=3, sticky="w", padx=(24,0))

        measureTitle=ctk.CTkLabel(master=self.resumeTab.tab(self.service.reminders[key]['name']), text=f"Progression actuelle : {self.service.reminders[key]['_currentMeasure']}")
        measureTitle.grid(row=4, sticky="w", padx=(24,0))

        deleteBtn = ctk.CTkButton(master=self.resumeTab.tab(self.service.reminders[key]['name']), text=f"Supprimer ce rappel", fg_color=Colors.darkBtnColor, hover_color=Colors.hghColor, 
                                command= lambda id=key : self.deleteTab(id))
        deleteBtn.place(x=275, y=237, anchor="se")

    def openNewReminder(self):
        if ((self.newReminderWindow == None) or (not self.newReminderWindow.winfo_exists())):
            self.newReminderWindow = NewReminder(self.root)
            self.newReminderWindow.service = self.service
        else:
            self.newReminderWindow.focus() 


    def deleteTab(self,id):
        self.service.delete(id)
        self.resumeTab.delete(self.resumeTab.get())


    def close(self):
        self.root.quit()
        sys.exit(0)
        # self.root.iconify()
        #PLUS DESACTIVER SCHEDULER


if __name__ == '__main__':
    ResumeInterface()
    