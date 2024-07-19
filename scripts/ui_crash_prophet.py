import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from keras.models import load_model
import numpy as np
import joblib
import json
import dotenv
import os
import boto3
from keras.models import load_model
import logging

DOTENV_PATH = os.environ.get('DOTENV_PATH', './../.env')

if dotenv.load_dotenv(dotenv_path=DOTENV_PATH) == False:
    print(f'no environment have been loaded from .env path \"{DOTENV_PATH}\"')

DICT_JSON_FILEPATH = '../data/dataset.metadata.json'
pred_list = ["Dual carriageway", "One way street", "Roundabout", "Single carriageway", "Slip road"]
IMPORTED_DATASET_S3_KEY = os.environ.get('IMPORTED_DATASET_S3_KEY', '')
IMPORTED_CNN_S3_KEY = os.environ.get('IMPORTED_CNN_S3_KEY', '')
S3_BUCKET_NAME = os.environ.get('BUCKET_NAME', 'pink-twins-bucket')
S3_IMAGES_BUCKET_FOLDER = os.environ.get('S3_IMAGES_BUCKET_FOLDER', '')
S3_BUCKET_FOLDER = os.environ.get('S3_MODELS_BUCKET_FOLDER', '')
S3_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY_ID', '')
S3_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY', '')
TMP_DIR = os.environ.get('TMP_DIR', '/tmp/pink-twins')

with open(DICT_JSON_FILEPATH) as json_file:
    dic = json.load(json_file)

def conversion(dic, word, category):
    value = dic[category][word]
    return value

try:
    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY_ID, aws_secret_access_key=S3_SECRET_ACCESS_KEY)
    imported_model_id = IMPORTED_CNN_S3_KEY.split('/')[-1]
    imported_model_file = f'{TMP_DIR}/{imported_model_id}'

    # Download the dump file from S3
    response = s3.download_file(Bucket=S3_BUCKET_NAME, Key=IMPORTED_CNN_S3_KEY,
        Filename=imported_model_file)

    cnn_model = load_model(imported_model_file)

except Exception as err:
    logging.fatal(f'failed to load dataset {IMPORTED_CNN_S3_KEY} from S3 bucket: {err}')


def open_image():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg")])
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)

        image_label.config(image=photo)
        image_label.image = photo

        return image

def classify_image():
    global photo, cnn_model

    selected_image = open_image()

    if selected_image:
        # Preprocess the image (adjust according to your CNN model's requirements)
        input_image = selected_image.convert("RGB")
        input_image = np.array(selected_image.resize((224, 224)))  # Assuming input size is 224x224
        input_image = input_image / 255.0  # Normalize pixel values
        input_image = np.expand_dims(input_image, axis=0)  # Add batch dimension

        # Use the CNN model to make predictions
        predictions = cnn_model.predict(input_image)
        # Modify the code to handle the predictions as needed
        # For example, you might want to display the predicted class or probabilities

        # Access the global variable for the PhotoImage object
        photo = ImageTk.PhotoImage(selected_image)

        # Display the input values from the text entry fields
        forest = joblib.load('scripts/random_forest.h5')
        wheather = wheather_entry.get()
        time = time_entry.get()
        day = day_entry.get()
        month = month_entry.get()
        year = year_entry.get()
        speed = speed_entry.get()
        light = light_entry.get()
        road = road_entry.get()
        rural = rural_entry.get()
        road_type = pred_list[np.argmax(predictions[0])]
        road_type = dic['Road_Type'][road_type]
        light = dic['Light_Conditions'][light]
        weather = dic['Weather_Conditions'][weather]
        road = dic['Road_Surface_Conditions'][road]
        if rural == "rural":
            rural = 1
        else :
            rural = 2

        vec = [[day,time,road_type,speed,light,wheather,road,rural,year,month]]
        answer = forest.predict(vec)
        print(answer)
        answer_label.config(text=f"Answer: {answer}")


window = tk.Tk()
window.title("Image Viewer and Classifier")
window.geometry("500x500")

# Entry fields for user input
wheather_label = tk.Label(window, text="Wheather:")
wheather_label.pack()

weather_options = ["Fine with high winds", "Snowing without high winds", "Fine without high winds", "Raining with high winds", "Raining without high winds", "Snowing with high winds", "Fog or mist", "Other", "Unknown"]
wheather_entry = ttk.Combobox(window, values=weather_options,width=50)
wheather_entry.pack()
# wheather_entry = tk.Entry(window)
# wheather_entry.pack()

time_label = tk.Label(window, text="Time:")
time_label.pack()
time_entry = tk.Entry(window, width=50)
time_entry.pack()

day_label = tk.Label(window, text="Day (in number):")
day_label.pack()
day_entry = tk.Entry(window,width=50)
day_entry.pack()

month_label = tk.Label(window, text="Month:")
month_label.pack()
month_entry = tk.Entry(window,width=50)
month_entry.pack()

year_label = tk.Label(window, text="Year:")
year_label.pack()
year_entry = tk.Entry(window,width=50)
year_entry.pack()

speed_label = tk.Label(window, text="Speed limit:")
speed_label.pack()
speed_entry = tk.Entry(window,width=50)
speed_entry.pack()

light_label = tk.Label(window, text="Light condition:")
light_label.pack()
light_options = ["Daylight: Street light present", "Darkness: Street lights present but unlit", "Darkeness: No street lighting", "Darkness: Street lighting unknown", "Darkness: Street lights present and lit"]
light_entry = ttk.Combobox(window, values=light_options,width=50)
light_entry.pack()

road_label = tk.Label(window, text="Road surface condition:")
road_label.pack()
road_options = ["Snow", "Flood (Over 3cm of water)", "Dry", "Normal", "Wet/Damp", "Frost/Ice"]
road_entry = ttk.Combobox(window, values=road_options,width=50)
road_entry.pack()

rural_label = tk.Label(window, text="Urban or Rural:")
rural_label.pack()
rural_options = ["Urban", "Rural"]
rural_entry = ttk.Combobox(window, values=rural_options,width=50)
rural_entry.pack()

# open_button = tk.Button(window, text="Open Image", command=open_image)
# open_button.pack(pady=10)

image_label = tk.Label(window)
image_label.pack()

classify_button = tk.Button(window, text="Classify Image", command=classify_image)
classify_button.pack(pady=10)

answer_label = tk.Label(window, text="Answer: ")
answer_label.pack()

window.mainloop()
