from ultralytics import YOLO

model = YOLO(r"KRAI\rak-v2\weights\best.pt")

# Export the model
model.export(format="openvino",half=True,int8=True)  # creates 'yolo26n_openvino_model/'

# Load the exported OpenVINO model
# ov_model = YOLO("yolo26n_openvino_model/")
