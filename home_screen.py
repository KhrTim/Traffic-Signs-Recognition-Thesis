import tkinter as tk
from tkinter import ttk
from camera_input_screen import CameraInputScreen
from file_input_screen import FileInputScreen
from model_types import ModelTypes
import customtkinter as ctk


class HomeScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Traffic Assistant")
        task_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame = ctk.CTkFrame(task_frame,fg_color="transparent")
        mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        radio_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")

        helper_lbl_1 = ctk.CTkLabel(task_frame, text="Mode")
        helper_lbl_1.pack(pady=20)

        helper_lbl_2 = ctk.CTkLabel(radio_frame, text="Image Source")
        helper_lbl_2.pack(pady=20)

        sign_detection_btn = ctk.CTkButton(
            button_frame, text="Traffic Signs", command=lambda: self.openWindow(ModelTypes.TRAFFIC_SIGNS))
        sign_detection_btn.pack(side=tk.LEFT, padx=10)
        road_markings_detection_btn = ctk.CTkButton(
            button_frame, text="Road Markings", command=lambda: self.openWindow(ModelTypes.ROAD_MARKINGS))
        road_markings_detection_btn.pack(side=tk.LEFT, padx=10)
        traffic_signs_detection_btn = ctk.CTkButton(
            button_frame, text="Traffic Lights", command=lambda: self.openWindow(ModelTypes.TRAFFIC_LIGHTS))
        traffic_signs_detection_btn.pack(side=tk.LEFT, padx=10)

        self.phone = tk.StringVar(value='file')
        home = ctk.CTkRadioButton(radio_frame, text='Camera',
                               variable=self.phone, value='camera')
        home.pack(side=tk.LEFT, padx=10)
        office = ctk.CTkRadioButton(
            radio_frame, text='File', variable=self.phone, value='file')
        office.pack(side=tk.LEFT, padx=10)
        radio_frame.pack()
        button_frame.pack()

        task_frame.pack(pady=20, expand=True)
        mode_frame.pack(side=tk.TOP, pady=20, expand=True)

    def openWindow(self, model_type):
        if self.phone.get() == 'camera':
            CameraInputScreen(self, model_type)
        else:
            FileInputScreen(self, model_type)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    home = HomeScreen()
    home.resizable()
    home.mainloop()
