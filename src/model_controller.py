import torch


class ModelController:
    def __init__(self, model_path=None):
        self.model = self.load_model(model_path)
        self.model.max_det = 10
        self.classes = self.model.names

    def load_model(self, model_name):
        assert model_name
        if model_name:
            model = torch.hub.load(
                "ultralytics/yolov5",
                "custom",
                path=model_name,
                device="cpu",
                force_reload=True,
            )
        return model

    def get_model(self):
        return self.model

    def get_classes(self):
        return self.classes
