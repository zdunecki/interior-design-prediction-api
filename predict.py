import tensorflow as tf
import numpy as np
import json
import argparse
from io import BytesIO

import urllib.request

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


url = "https://scontent.fpoz2-1.fna.fbcdn.net/v/t1.0-9/78450257_2561393933914551_5972082700020875264_o.jpg?_nc_cat=100&_nc_ohc=7LQR1ha7bG4AQn7-BeyuiYhwFKvzd3_lL1P_Nm7PLUzN_9VqWJJOweU3g&_nc_ht=scontent.fpoz2-1.fna&oh=7eb51898afa07d075625d0f71b2ea30e&oe=5E7577F8";


def run_job():
    print(5)
    for _ in range(10):
        img_pred = load_image(url)
        result = predict_process(img_pred)
        values = result[0].tolist()

        # (prediction_score, label)
        sorted_match = list(map(lambda a: (a[1], labels[a[0]]), enumerate(values)))

        print(sorted_match)


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
