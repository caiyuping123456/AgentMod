from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Train the model on the COCO8 dataset for 100 epochs
train_results = model.train(
    data=r"D:\Py_Project\Langcahin\test\a\fire.yaml",  # Path to dataset configuration file
    epochs=100,  # Number of training epochs
    imgsz=640,  # Image size for training
    device="cpu",  # Device to run on (e.g., 'cpu', 0, [0,1,2,3])
)
# train_results = model.train(
#     data=r"D:\Py_Project\Langcahin\test\a\fire.yaml",
#     epochs=50,
#     imgsz=640,
#     device=0,  # 4060用0即可
#     amp=True,  # 4060必开，显存占用减少50%
#     batch=-1,  # 自动适配4060的8GB显存（通常会设为8/16）
# )

# Evaluate the model's performance on the validation set
metrics = model.val()

# Perform object detection on an image
results = model("path/to/image.jpg")  # Predict on an image
results[0].show()  # Display results

# Export the model to ONNX format for deployment
path = model.export(format="onnx")  # Returns the path to the exported model