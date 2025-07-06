import customtkinter as ctk
from geometryCalcutator import set
from colors import Colors

class ReminderInterface:

    reminder = None
    root = None
    answer = None
    service = None

    def __init__(self, reminder, service):
        self.reminder = reminder
        self.service = service
        self.root = ctk.CTkToplevel()
        self.answer = ctk.StringVar(self.root, "Non")
        self.amount = ctk.StringVar(self.root, "")
        self.window()

    def window(self):
        # Window
        self.root.title("Rappel")
        self.root.geometry(set(500, 200))
        self.root.resizable(False,False)
        self.root.attributes('-topmost', 'true')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=2)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Title
        headFrame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        headFrame.grid(row=0, sticky="ns", pady=(12,0))

        headTitle = ctk.CTkLabel(master=headFrame, text="Avez-vous pensé à... ", font=ctk.CTkFont(size=18, weight="bold"))
        headTitle.grid(sticky="ns", row=0)
        subheadTitle = ctk.CTkLabel(master=headFrame, text="Boire de l'eau ?", font=ctk.CTkFont(size=14, weight="bold"))
        subheadTitle.grid(sticky="ns", row=1)

        # Reponse utilisateur
        self.answerFrame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        self.answerFrame.grid_columnconfigure(0, weight=1)
        self.answerFrame.grid_columnconfigure(1, weight=1)
        self.answerFrame.grid_columnconfigure(2, weight=1)
        self.answerFrame.grid(row=1, column=0)

        noBtn = ctk.CTkRadioButton(master=self.answerFrame, width=100, variable=self.answer, value="Non", text="Non",  command=self.changeAmountStatut, fg_color="lightgrey", hover_color=Colors.hghColor)
        noBtn.grid(row=0, column=0)

        yesBtn = ctk.CTkRadioButton(master=self.answerFrame, variable=self.answer, value="Oui", text="Oui (Quelle quantité ?) :  ", command=self.changeAmountStatut, fg_color="lightgrey", hover_color=Colors.hghColor)
        yesBtn.grid(row=0, column=1)

        self.amountInput = ctk.CTkEntry(master=self.answerFrame, state="disabled", textvariable=self.amount)
        self.amountInput.grid(row=0, column=2)


        # Bouttons
        buttonsFrame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        buttonsFrame.grid(row=3, sticky="ew")
        buttonsFrame.grid_columnconfigure(0, weight=1)

        validateBtn = ctk.CTkButton(master=buttonsFrame, text="Valider", fg_color=Colors.darkBtnColor, hover_color=Colors.hghColor, command=self.validate)
        validateBtn.grid()

        # self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)


    def changeAmountStatut(self):
        if (self.answer.get() == "Non"):
            self.amountInput.configure(state="disabled", text_color="grey", border_color="grey")
        else:
            self.amountInput.configure(state="normal", text_color="black", border_color=Colors.btnColor)


    def validate(self):
        if (self.answer == "Non"):
            self.service.validateReminder(self.reminder['id'], 0)
        else:
            self.service.validateReminder(self.reminder['id'], self.amountInput.get())
        print(self.answer.get())
        self.root.destroy()


if __name__ == '__main__':
    ReminderInterface()