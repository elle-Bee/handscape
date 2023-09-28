import uuid
import time
import os
import cv2
import shutil
import subprocess

BASE_PATH = "assets"
IMAGEDATA_PATH = os.path.join(BASE_PATH, "imagedata")
LABELIMG_PATH = os.path.join(BASE_PATH, "labelImg")

if not os.path.exists(LABELIMG_PATH):
    os.makedirs(LABELIMG_PATH, exist_ok=True)
    subprocess.run(["git", "clone", "https://github.com/tzutalin/labelImg", LABELIMG_PATH])

def clean_folder_name(name):
    return "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in name)

def collect_images_for_label(label):
    folder_name = clean_folder_name(label)
    folder_path = os.path.join(IMAGEDATA_PATH, folder_name)

    try:
        os.makedirs(folder_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder '{folder_path}': {e}")
        return

    cap = cv2.VideoCapture(0)
    frame_width = 1920
    frame_height = 1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    print(f"Collecting images for {label}")
    time.sleep(5)

    capture_count = 10

    for num in range(capture_count):
        ret, frame = cap.read()
        image_name = os.path.join(folder_path, '{}_{}.jpg'.format(folder_name, str(uuid.uuid1())))
        cv2.imwrite(image_name, frame)
        cv2.imshow('frame', frame)
        time.sleep(3)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return folder_name



labels = []

while True:
    new_label = input("Enter the new label you want to create: ")
    collected_label_folder = collect_images_for_label(new_label)
    labels.append(collected_label_folder)

    add_more = input("Do you want to add more labels? (yes/no): ").lower()
    if add_more != 'yes':
        break

for folder in labels:
    folder_path = os.path.join(IMAGEDATA_PATH, folder)

    if not os.path.isdir(folder_path):
        continue

    cleaned_folder_name = clean_folder_name(folder)

    files_in_folder = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file in files_in_folder:
        source_path = os.path.join(folder_path, file)
        destination_path = os.path.join(IMAGEDATA_PATH, f"{cleaned_folder_name}_{file}")

        shutil.move(source_path, destination_path)

    os.rmdir(folder_path)

print("Images moved to the main imagedata directory.")

TESTING_PATH = os.path.join(IMAGEDATA_PATH, "testing")
TRAINING_PATH = os.path.join(IMAGEDATA_PATH, "training")
ANNOTATIONS_PATH = os.path.join(BASE_PATH, "annotations")
MODEL_PATH = os.path.join(BASE_PATH, "model")
for path in [TESTING_PATH, TRAINING_PATH, ANNOTATIONS_PATH, MODEL_PATH]:
    os.makedirs(path, exist_ok=True)
