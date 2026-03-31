import cv2
import os
import numpy as np
from PIL import Image

dataset_path = "dataset"
trainer_path = "trainer"
os.makedirs(trainer_path, exist_ok=True)

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []

    for image_path in image_paths:
        gray_img = Image.open(image_path).convert("L")
        img_np = np.array(gray_img, "uint8")

        # Filename format: User.id.count.jpg
        user_id = int(os.path.split(image_path)[-1].split(".")[1])

        faces = face_cascade.detectMultiScale(img_np)
        for (x, y, w, h) in faces:
            face_samples.append(img_np[y:y+h, x:x+w])
            ids.append(user_id)

    return face_samples, ids

print("Training model... please wait.")
faces, ids = get_images_and_labels(dataset_path)
recognizer.train(faces, np.array(ids))

recognizer.save("trainer/trainer.yml")
print("Model trained and saved at trainer/trainer.yml")
