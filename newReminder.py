import customtkinter as ctk
import tkinter as tk
from geometryCalcutator import set
from colors import Colors

# ctk.set_appearance_mode("light")

class NewReminder(ctk.CTkToplevel):

    service = None
    root = None

    def __init__(self, *args):
        super().__init__(*args)
        self.root=self
        
        # Window
        self.root.title("Nouveau rappel")
        self.root.geometry(set(370, 400))
        self.root.resizable(False,False)
        self.root.focus()
        # self.root.iconphoto(False,"icon.png")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=2)
        self.root.grid_columnconfigure(0, weight=1)


        # Values
        startHour:int = ctk.IntVar(value=8)
        startMin:int = ctk.IntVar(value=00)
        endHour:int = ctk.IntVar(value=17)
        endMin:int = ctk.IntVar(value=00)


        # Naming
        nameFrame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        nameFrame.grid(row=0, sticky="ew", padx=24)
        nameFrame.grid_columnconfigure(0, weight=1)

        nameTitle = ctk.CTkLabel(master=nameFrame, text="Nommez votre rappel")
        nameTitle.grid(row=0)
        self.nameInput = ctk.CTkEntry(master=nameFrame, placeholder_text="Nom...", border_color=Colors.mainColor)
        self.nameInput.grid(row=1, sticky="we")

        # Period choose
        periodFrame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        periodFrame.grid(row=1, sticky="ew", padx=24)
        periodFrame.grid_columnconfigure(0, weight=1)
        periodFrame.grid_columnconfigure(1, weight=1)

        periodTitle = ctk.CTkLabel(master=periodFrame, text="Choisissez la période du rappel").grid(row=0, columnspan=2)

        #------- Start
        periodStartFrame = ctk.CTkFrame(master=periodFrame, fg_color=Colors.mainColor)
        periodStartFrame.grid(row=1, column=0, rowspan=2, sticky="ew", padx=(0, 8))
        periodStartFrame.grid_columnconfigure(0, weight=10)
        periodStartFrame.grid_columnconfigure(1, weight=1)
        periodStartFrame.grid_columnconfigure(2, weight=10)

        periodStartTitle = ctk.CTkLabel(master=periodStartFrame, text="Début")
        periodStartTitle.grid(row=0, pady=(4,0), sticky="ew", columnspan=3)

        self.hourStartSpinbox = tk.Spinbox(master=periodStartFrame, from_=0, to=23, textvariable=startHour, wrap=True, width=8)
        self.hourStartSpinbox.grid(row=1, column=0)
        ctk.CTkLabel(master=periodStartFrame, text=" : ").grid(row=1, column=1)
        self.minuteStartSpinbox = tk.Spinbox(master=periodStartFrame,from_=00, to=59, textvariable=startMin, wrap=True, width=8)
        self.minuteStartSpinbox.grid(row=1, column=2)

        #------- End
        periodEndFrame = ctk.CTkFrame(master=periodFrame, fg_color=Colors.mainColor)
        periodEndFrame.grid(row=1, column=1, rowspan=2, sticky="ew", padx=(8,0))
        periodEndFrame.grid_columnconfigure(0, weight=10)
        periodEndFrame.grid_columnconfigure(1, weight=1)
        periodEndFrame.grid_columnconfigure(2, weight=10)

        periodEndTitle = ctk.CTkLabel(master=periodEndFrame, text="Fin")
        periodEndTitle.grid(row=0, pady=(4,0), columnspan=3)

        self.hourEndSpinbox = tk.Spinbox(master=periodEndFrame, from_=0, to=23, textvariable=endHour, wrap=True, width=8)
        self.hourEndSpinbox.grid(row=1, column=0)
        ctk.CTkLabel(master=periodEndFrame, text=" : ").grid(row=1, column=1)
        self.minuteEndSpinbox = tk.Spinbox(master=periodEndFrame,from_=00, to=59, textvariable=endMin, wrap=True, width=8)
        self.minuteEndSpinbox.grid(row=1, column=2)


        # Counting
        countersFrame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        countersFrame.grid(row=2, sticky="we", padx=24)
        countersFrame.grid_columnconfigure(0, weight=1)
        countersFrame.grid_columnconfigure(1, weight=1)

        countersTitle = ctk.CTkLabel(master=countersFrame, text="Informations supplémentaires", fg_color="transparent")
        countersTitle.grid(row=0, columnspan=2)

        #------- count
        countFrame = ctk.CTkFrame(master=countersFrame)
        countFrame.grid(row=1, column=0, sticky="ew", padx=(0,8))
        countFrame.grid_columnconfigure(0, weight=1)

        countTitle = ctk.CTkLabel(master=countFrame, text="Nombre de rappels", fg_color="transparent")
        countTitle.grid(row=0, pady=(4,0))
        self.countInput = ctk.CTkEntry(master=countFrame, placeholder_text="Nombre...", width=80, border_color=Colors.mainColor)
        self.countInput.grid(row=1, pady=(0,8))

        #------- measure
        measureFrame = ctk.CTkFrame(master=countersFrame)
        measureFrame.grid(row=1, column=1, sticky="ewns", padx=(8,0))
        measureFrame.grid_columnconfigure(0, weight=1)

        measureTitle = ctk.CTkLabel(master=measureFrame, text="Objectif", fg_color="transparent")
        measureTitle.grid(row=0, pady=(4,0))
        self.measureInput = ctk.CTkEntry(master=measureFrame, placeholder_text="Valeur...", width=80, border_color=Colors.mainColor)
        self.measureInput.grid(row=1, pady=(0,8))


        # Buttons
        buttonsFrame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        buttonsFrame.place(x=330, y=380, anchor="se")

        cancelBtn = ctk.CTkButton(master=buttonsFrame, text="Annuler", width=80, height=28, fg_color=Colors.btnColor , hover_color=Colors.hghColor, command=self.root.destroy)
        cancelBtn.pack(side="left")
        validateBtn = ctk.CTkButton(master=buttonsFrame, text="Valider", width=80, fg_color=Colors.darkBtnColor, hover_color=Colors.hghColor,
                                    command= self.validate)                                      
        validateBtn.pack(side="left", padx=(12,0))

        self.root.after(201, lambda :self.root.iconbitmap('icon.ico'))

    def validate(self):
        self.service.save(self.nameInput.get(), 
                          self.hourStartSpinbox.get(), 
                          self.minuteStartSpinbox.get(), 
                          self.hourEndSpinbox.get(),
                          self.minuteEndSpinbox.get(),
                          self.countInput.get(),
                          self.measureInput.get(), 
                          self)

        ## METHODDE UPDATE ICI

        