import customtkinter as ctk

from src.home_screen import HomeScreen

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    home = HomeScreen()
    home.resizable()
    home.mainloop()
