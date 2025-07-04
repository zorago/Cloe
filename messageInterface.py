import customtkinter as ctk
from geometryCalcutator import set
from colors import Colors

class MessageInterface:

    def __init__(self, message:str):
        self.messageBox = ctk.CTkToplevel()
        self.messageBox.title("Information")

        self.messageBox.geometry(set(400, 140))
        self.messageBox.resizable(False, False)
        self.messageBox.attributes('-topmost', 'true')

        self.messageBox.grid_rowconfigure(0, weight=1)
        self.messageBox.grid_rowconfigure(1, weight=1)
        self.messageBox.grid_rowconfigure(2, weight=3)
        self.messageBox.grid_rowconfigure(3, weight=3)
        self.messageBox.grid_columnconfigure(0, weight=1)

        self.headerTitle = ctk.CTkLabel(master=self.messageBox, text="Attention", font=ctk.CTkFont(size=16))
        self.headerTitle.grid(row=0, pady=(12,0))

        self.messageTitle = ctk.CTkLabel(master=self.messageBox, text=message)
        self.messageTitle.grid(row=1)

        self.cancelBtn = ctk.CTkButton(master=self.messageBox, text="Compris", fg_color=Colors.darkBtnColor, hover_color=Colors.hghColor, command=self.messageBox.destroy)
        self.cancelBtn.grid(row=3)



class ValidationMessageInterface(MessageInterface):

    def __init__(self, message, parentWindow):
        super().__init__(message)
        self.parentWindow = parentWindow
        self.messageBox.title("Confirmation")
        self.headerTitle.configure(text="C'est tout bon !")
        self.cancelBtn.configure(command=self.closeAll)

    def closeAll(self):
        self.messageBox.destroy()
        self.parentWindow.root.destroy()