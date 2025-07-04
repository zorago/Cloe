import customtkinter as ctk

def set(widht:int, height:int):
    screen = ctk.CTk()
    screenWidth = screen.winfo_screenwidth()
    screenHeight = screen.winfo_screenheight()
    windowWidth = widht
    windowHeight = height
    windowPosX = (screenWidth-windowWidth)/2
    windowPosY = (screenHeight-windowHeight)/2

    return f"{windowWidth}x{windowHeight}+{int(windowPosX)}+{int(windowPosY)}"