import tensorflow as tf
import numpy as np
import json
import argparse
import os
import urllib.request

from io import BytesIO
from pymongo import MongoClient

client = MongoClient(os.environ.get('MONGO_URL', 'mongodb://localhost:28017'))
db = client["topify"]

labels = [
    "bohemian",
    "classic",
    "coastal",
    "farm-house",
    "glam",
    "industrial",
    "mid-century-modern",
    "minimal",
    "preppy",
    "rustic",
    "scandinavian",
    "transitional"
]


def load_image(endpoint):
    try:
        with urllib.request.urlopen(endpoint) as u:
            img = tf.keras.preprocessing.image.load_img(BytesIO(u.read()), target_size=(150, 150))

            return tf.keras.preprocessing.image.img_to_array(img)

    except urllib.error.HTTPError as e:
        print("ERROR")


def predict_process(img):
    pred = tf.keras.preprocessing.image.img_to_array(img)

    pred = np.expand_dims(pred, axis=0)
    pred = pred / 255

    return model.predict(pred)

# TODO logger
def run_job():
    creators = db["creators"].find()
    predictions_col = db["predictions"]

    for creator in creators:
        if not ("images" in creators):
            continue

        images = creator["images"]

        for img in images:
            if not ("url" in img):
                continue

            url = img["url"]
            already_predicted = predictions_col.find_one({"input": url})

            # TODO: catch case if input already predicted but with specific interior style
            if already_predicted:
                continue

            img_pred = load_image(url)
            result = predict_process(img_pred)
            predictions = result[0].tolist()

            for (index, prediction) in enumerate(predictions):
                label = labels[index]

                basic_data = {
                    "label": "interior_style." + label,
                    "input": url,
                    "creatorId": creator["id"]
                }

                existing = predictions_col.find_one(basic_data)

                if existing:
                    predictions_col.update_one(basic_data, {"$set": {"score": prediction}})
                else:
                    new_data = basic_data
                    new_data["score"] = prediction

                    predictions_col.insert_one(basic_data)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model-path',
        type=str,
        default="./data/model.h5",
        help='model path'
    )
    parser.add_argument(
        '--weights-path',
        type=str,
        help='model path'
    )
    a, _ = parser.parse_known_args()
    return a


if __name__ == '__main__':
    args = get_args()

    if args.weights_path:
        with open(args.model_path, 'r') as f:
            model_json = json.dumps(json.load(f))

            model = tf.keras.models.model_from_json(model_json)
            model.load_weights(args.weights_path)
    else:
        model = tf.keras.models.load_model(args.model_path)

    run_job()
