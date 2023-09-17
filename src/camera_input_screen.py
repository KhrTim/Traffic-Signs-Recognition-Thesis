import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageTk

from src.detector import ObjectDetector
from src.model_controller import ModelController
from src.model_types import ModelTypes
from src.source_controller import SourceController
from src.source_mode import SourceMode


class CameraInputScreen(ctk.CTkToplevel):
    def __init__(self, parent, model_type: ModelTypes):
        super().__init__(parent)
        # self.grab_set()
        self.title("Camera input analysis")

        back_asset = Image.open("./assets/home_FILL0_wght400_GRAD0_opsz48.png")
        back_asset = ImageTk.PhotoImage(back_asset)
        if model_type == ModelTypes.TRAFFIC_SIGNS:
            self.model_controller = ModelController("./traffic_signs_detection.pt")
        elif model_type == ModelTypes.TRAFFIC_LIGHTS:
            self.model_controller = ModelController("./traffic_lights_detection.pt")
        elif model_type == ModelTypes.ROAD_MARKINGS:
            self.model_controller = ModelController("./road_markings_detection.pt")
        self.source_controller = SourceController(SourceMode.CAMERA)
        self.object_detector = ObjectDetector(self.model_controller)

        img = self.object_detector.get_labeled_image(
            self.source_controller.return_latest_frame()
        )
        imgtk = ImageTk.PhotoImage(img)

        image_frame = ctk.CTkFrame(self, width=1200, height=800, fg_color="transparent")
        self.img_widget = ctk.CTkLabel(image_frame, image=imgtk, text=None)
        self.img_widget.after(20, self.update_frame)

        self.img_widget.pack(expand=True, fill=tk.BOTH)
        image_frame.pack(padx=20, pady=20)

        button_frame = ctk.CTkFrame(self)

        go_back_button = ctk.CTkButton(
            button_frame, command=self.destroy_window, image=back_asset, text=None
        )
        go_back_button.pack(padx=20, pady=20)
        button_frame.pack(expand=True, fill=tk.X)
        self.grab_set()

    def destroy_window(self):
        self.source_controller.clear()
        self.destroy()

    def update_frame(self):
        img = self.object_detector.get_labeled_image(
            self.source_controller.return_latest_frame()
        )
        imgtk = ImageTk.PhotoImage(img)
        self.img_widget.configure(image=imgtk)
        self.img_widget.image = imgtk
        self.img_widget.after(20, self.update_frame)
