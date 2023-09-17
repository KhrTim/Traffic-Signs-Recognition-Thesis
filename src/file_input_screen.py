import os
import tkinter as tk
from tkinter import filedialog as fd

import customtkinter as ctk
from PIL import Image, ImageTk

from src.detector import ObjectDetector
from src.model_controller import ModelController
from src.model_types import ModelTypes
from src.source_controller import SourceController
from src.source_mode import SourceMode


class FileInputScreen(ctk.CTkToplevel):
    def __init__(self, parent, model_type: ModelTypes):
        super().__init__(parent)
        self.geometry("1400x900")

        self.title("Saved files analysis")
        back_asset = Image.open("./assets/home_FILL0_wght400_GRAD0_opsz48.png")
        back_asset = ImageTk.PhotoImage(back_asset)
        load_asset = Image.open("./assets/search_FILL0_wght400_GRAD0_opsz48.png")
        load_asset = ImageTk.PhotoImage(load_asset)
        if model_type == ModelTypes.TRAFFIC_SIGNS:
            self.model_controller = ModelController("./traffic_signs_detection.pt")
        elif model_type == ModelTypes.TRAFFIC_LIGHTS:
            self.model_controller = ModelController("./traffic_lights_detection.pt")
        elif model_type == ModelTypes.ROAD_MARKINGS:
            self.model_controller = ModelController("./road_markings_detection.pt")

        self.object_detector = ObjectDetector(self.model_controller)
        self.source_controller = None

        image_frame = ctk.CTkFrame(self, width=1200, height=800, fg_color="transparent")
        self.img_widget = ctk.CTkLabel(image_frame, text=None)
        if (
            self.source_controller
            and self.source_controller.current_mode() == SourceMode.VIDEO
        ):
            self.img_widget.after(20, self.update_frame)

        self.img_widget.pack(expand=True, fill=tk.BOTH)
        image_frame.pack(padx=20, pady=20)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")

        go_back_button = ctk.CTkButton(
            button_frame, command=self.destroy_window, image=back_asset, text=None
        )
        go_back_button.pack(side=tk.LEFT, padx=20, pady=20)

        get_source_button = ctk.CTkButton(
            button_frame, command=self.choose_file, image=load_asset, text=None
        )
        get_source_button.pack(side=tk.RIGHT, padx=20, pady=20)

        button_frame.pack(expand=True, fill=tk.X)
        self.grab_set()

    def destroy_window(self):
        if self.source_controller:
            self.source_controller.clear()
        self.destroy()

    def choose_file(self):
        filetypes = (
            ("Image", "*.jpg"),
            ("Image", "*.jpeg"),
            ("Image", "*.ppm"),
            ("Image", "*.png"),
            ("Video", "*.mp4"),
        )

        filename = fd.askopenfilename(
            title="Open a file", initialdir=".", filetypes=filetypes
        )
        self.change_source_controller(filename)
        self.update_frame()

    def change_source_controller(self, filename):
        _, file_extension = os.path.splitext(filename)
        if (
            not self.source_controller
            or self.source_controller.current_filename() != filename
        ):
            if self.source_controller:
                self.source_controller.clear()
            if file_extension == ".mp4":
                self.source_controller = SourceController(
                    SourceMode.VIDEO, source_path=filename
                )
            else:
                self.source_controller = SourceController(
                    SourceMode.IMAGE, source_path=filename
                )

    def update_frame(self):
        img = self.object_detector.get_labeled_image(
            self.source_controller.return_latest_frame()
        )
        imgtk = ImageTk.PhotoImage(img)
        self.img_widget.configure(image=imgtk)
        self.img_widget.image = imgtk
        if self.source_controller.current_mode() == SourceMode.VIDEO:
            self.img_widget.after(20, self.update_frame)
