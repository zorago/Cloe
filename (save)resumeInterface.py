import customtkinter as ctk
from geometryCalcutator import set
from colors import Colors

class ResumeInterface:

    service = None
    root = ctk.CTk()

    def __init__(self, service): 

        self.service = service()
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
        headTitle = ctk.CTkLabel(master=headFrame, text="rememberMe", font=ctk.CTkFont(size=24, weight="bold"))
        headFrame.grid_rowconfigure(0, weight=1)
        headTitle.grid(sticky="ns")

        addBtn = ctk.CTkButton(master=self.root, text="Add")
        addBtn.place(x=10, y=10, anchor="nw")

        # Resume
        resumeTab = ctk.CTkTabview(master=self.root, height=300, segmented_button_selected_color=Colors.btnColor, segmented_button_selected_hover_color=Colors.hghColor)
        resumeTab.grid(row=1)
        resumeTab.grid_columnconfigure(0, weight=1)

        for key in self.service.reminders:

            resumeTab.add(self.service.reminders[key]['name'])

            startTitle=ctk.CTkLabel(master=resumeTab.tab(self.service.reminders[key]['name']), 
                                    text=f"A commencé à {self.service.reminders[key]['startTime'].strftime("%H")} h {self.service.reminders[key]['startTime'].strftime("%M")}")
            startTitle.grid(row=1, sticky="w", padx=(24,0), pady=(24,0))

            endTitle=ctk.CTkLabel(master=resumeTab.tab(self.service.reminders[key]['name']), 
                                text=f"Se termine à {self.service.reminders[key]['endTime'].strftime("%H")} h {self.service.reminders[key]['endTime'].strftime("%M")}")
            endTitle.grid(row=2, sticky="w", padx=(24,0))

            countTitle=ctk.CTkLabel(master=resumeTab.tab(self.service.reminders[key]['name']), text=f"Nombre de rappel à venir : {self.service.reminders[key]['count']}")
            countTitle.grid(row=3, sticky="w", padx=(24,0))

            measureTitle=ctk.CTkLabel(master=resumeTab.tab(self.service.reminders[key]['name']), text=f"Décompte restant : {self.service.reminders[key]['measure']}")
            measureTitle.grid(row=4, sticky="w", padx=(24,0))

            deleteBtn = ctk.CTkButton(master=resumeTab.tab(self.service.reminders[key]['name']), text=f"Supprimer ce rappel ({key})", fg_color=Colors.darkBtnColor, hover_color=Colors.hghColor, 
                                    command= lambda id=key : self.delete(id))
            deleteBtn.place(x=280, y=240, anchor="se")

        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        self.root.mainloop()


    def delete(self,id):
        self.service.delete(id)
        self.resumeTab.delete(self.resumeTab.get())
