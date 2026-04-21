from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
CLASS_NAMES_PATH = os.path.join(BASE_DIR, "class_names.json")
FRUIT_MODEL_PATH = os.path.join(BASE_DIR, "models", "fruit_model.h5")
FRUIT_CLASS_NAMES_PATH = os.path.join(BASE_DIR, "models", "fruit_class_names.json")
LEAF_MODEL_CANDIDATES = [
    os.path.join(BASE_DIR, "models", "leaf_model.keras"),
    os.path.join(BASE_DIR, "models", "leaf_model.h5"),
    os.path.join(BASE_DIR, "plant_model.h5"),
]

# Try to load TensorFlow and model
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TENSORFLOW_AVAILABLE = True

    model = None
    loaded_leaf_model_path = None
    for candidate in LEAF_MODEL_CANDIDATES:
        if not os.path.exists(candidate):
            continue
        try:
            model = tf.keras.models.load_model(candidate)
            loaded_leaf_model_path = candidate
            print(f"Loaded leaf model from {candidate}")
            break
        except Exception as e:
            print(f"Warning: Failed to load leaf model from {candidate}: {e}")

    if model is None:
        print(f"Warning: No leaf model file found. Checked: {LEAF_MODEL_CANDIDATES}")
except ImportError:
    TENSORFLOW_AVAILABLE = False
    model = None
    fruit_model = None
    load_model = None
    print("Warning: TensorFlow not available. Running in mock mode.")


def load_model_if_exists(model_path):
    if not TENSORFLOW_AVAILABLE:
        return None
    if os.path.exists(model_path):
        try:
            return load_model(model_path)
        except Exception as exc:
            print(f"Warning: Failed to load model {model_path}: {exc}")
            return None
    return None


FRUIT_MODEL_LOAD_ERROR = None


def load_fruit_model_safely():
    global FRUIT_MODEL_LOAD_ERROR
    if not TENSORFLOW_AVAILABLE:
        FRUIT_MODEL_LOAD_ERROR = "TensorFlow is not available in current Python environment."
        return None

    print("Loading fruit model...")
    if not os.path.exists(FRUIT_MODEL_PATH):
        FRUIT_MODEL_LOAD_ERROR = f"Fruit model file not found at {FRUIT_MODEL_PATH}"
        print(FRUIT_MODEL_LOAD_ERROR)
        return None

    try:
        loaded_model = load_model(FRUIT_MODEL_PATH)
        FRUIT_MODEL_LOAD_ERROR = None
        print("Model loaded successfully")
        return loaded_model
    except Exception as exc:
        FRUIT_MODEL_LOAD_ERROR = f"Failed to load fruit model: {exc}"
        print(FRUIT_MODEL_LOAD_ERROR)
        return None


fruit_model = load_fruit_model_safely()

if os.path.exists(CLASS_NAMES_PATH):
    with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
        CLASS_NAMES = json.load(f)
else:
    CLASS_NAMES = ["Unknown"]  # Fallback
    print(f"Warning: Class names file not found at {CLASS_NAMES_PATH}")

if os.path.exists(FRUIT_CLASS_NAMES_PATH):
    with open(FRUIT_CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
        FRUIT_CLASS_NAMES = json.load(f)
else:
    FRUIT_CLASS_NAMES = []
    print(f"Warning: Fruit class names file not found at {FRUIT_CLASS_NAMES_PATH}")

SOLUTIONS = {
    "Apple___Apple_scab": "Remove and destroy infected leaves. Spray a fungicide such as captan or myclobutanil at 7-10 day intervals during wet periods. Prune canopy for airflow and avoid overhead irrigation.",
    "Apple___Black_rot": "Prune infected twigs and remove mummified fruits. Spray a recommended fungicide (captan or mancozeb-based) on schedule. Keep orchard floor clean to reduce reinfection.",
    "Apple___Cedar_apple_rust": "Remove nearby juniper hosts if possible. Apply preventive fungicide at pink bud through petal-fall stages. Prune for airflow and monitor new lesions weekly.",
    "Apple___healthy": "Plant appears healthy. Continue routine scouting, balanced nutrition, and preventive sanitation.",
    "Potato___Early_blight": "Remove heavily infected lower leaves. Spray chlorothalonil or mancozeb as labeled. Maintain plant spacing and avoid prolonged leaf wetness.",
    "Potato___Late_blight": "Immediately remove infected plants/leaves and avoid moving wet foliage between fields. Apply late-blight specific fungicide (metalaxyl or cymoxanil mixes) as per label and repeat at short intervals in humid weather.",
    "Potato___healthy": "Plant appears healthy. Maintain crop rotation, balanced fertilizer, and regular scouting.",
    "Tomato___Tomato_mosaic_virus": "There is no curative spray for mosaic virus. Remove infected plants, disinfect tools and hands, control weeds, and use resistant seed/varieties in the next cycle."
}
IMAGE_SIZE = (224, 224)


def model_expects_normalized_input(loaded_model):
    first_layer = loaded_model.layers[0] if loaded_model and loaded_model.layers else None
    if first_layer and first_layer.__class__.__name__ == "Rescaling":
        return False
    return True


def preprocess_image(file_stream, loaded_model):
    image = Image.open(file_stream).convert("RGB")
    image = image.resize(IMAGE_SIZE)
    image_array = np.array(image, dtype=np.float32)
    if model_expects_normalized_input(loaded_model):
        image_array = image_array / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array


def predict_with_model(file_stream, loaded_model, class_names):
    image_tensor = preprocess_image(file_stream, loaded_model)
    predictions = loaded_model.predict(image_tensor, verbose=0)
    predictions = np.squeeze(predictions)

    if np.isscalar(predictions):
        predictions = np.array([float(predictions)], dtype=np.float32)

    predictions = np.asarray(predictions, dtype=np.float32)
    pred_sum = float(np.sum(predictions))
    if pred_sum > 0:
        predictions = predictions / pred_sum

    score = float(np.max(predictions)) if predictions.size else 0.0
    index = int(np.argmax(predictions)) if predictions.size else 0
    disease = class_names[index] if index < len(class_names) else f"class_{index}"
    return disease, score


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    file = request.files["image"]
    try:
        if not TENSORFLOW_AVAILABLE or model is None:
            # Mock prediction when TensorFlow/model not available
            return jsonify({
                "disease": "Mock: Tomato___healthy",
                "confidence": 0.85,
                "solution": "Trained leaf model was not loaded. Ensure python_api/models/leaf_model.keras exists and restart Flask API.",
                "note": "Fallback mock response"
            })

        disease, score = predict_with_model(file, model, CLASS_NAMES)

        solution = SOLUTIONS.get(
            disease,
            "This result comes from the trained plant disease model. If confidence is low, verify with a plant health expert."
        )

        return jsonify({
            "disease": disease,
            "confidence": score,
            "solution": solution
        })
    except Exception as exc:
        return jsonify({"error": f"Prediction failed: {str(exc)}"}), 500


@app.route("/predict-fruit", methods=["POST"])
def predict_fruit():
    print("[Python API] /predict-fruit request received")
    if "image" not in request.files:
        print("[Python API] Missing image in request")
        return jsonify({"error": "No image file provided."}), 400

    if not TENSORFLOW_AVAILABLE:
        print("[Python API] TensorFlow unavailable")
        return jsonify({"error": "Fruit model not loaded properly", "details": "TensorFlow is not available in current Python environment."}), 503

    if not os.path.exists(FRUIT_MODEL_PATH):
        missing_path_error = f"Fruit model file not found at {FRUIT_MODEL_PATH}"
        print(f"[Python API] {missing_path_error}")
        return jsonify({"error": "Fruit model not loaded properly", "details": missing_path_error}), 503

    if fruit_model is None:
        print("[Python API] fruit_model.h5 not loaded")
        return jsonify({
            "error": "Fruit model not loaded properly",
            "details": FRUIT_MODEL_LOAD_ERROR or "Unknown fruit model load error."
        }), 503

    if not FRUIT_CLASS_NAMES:
        print("[Python API] fruit_class_names.json missing or empty")
        return jsonify({"error": "Fruit model not loaded properly", "details": "fruit_class_names.json is missing or empty."}), 503

    try:
        file = request.files["image"]
        disease, confidence = predict_with_model(file, fruit_model, FRUIT_CLASS_NAMES)

        return jsonify({
            "disease": disease,
            "confidence": confidence,
            "suggestion": "Use crop-specific fungicide guidance for this fruit disease."
        })
    except Exception as exc:
        print(f"[Python API] Prediction error: {exc}")
        return jsonify({"error": "Fruit model not loaded properly", "details": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
