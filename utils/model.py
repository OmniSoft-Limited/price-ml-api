import onnxruntime as ort
import numpy as np

def load_model(filename: str):
    try:
        model = ort.InferenceSession(filename)
        print(f"ONNX model loaded from {filename}")
        return model
    except Exception as e:
        print(f"Something went wrong: {e}")

def run(model, X) -> float:
    input_name = model.get_inputs()[0].name
    X = np.array(X, dtype=np.float32).reshape(1, -1)
    prediction = model.run(None, {input_name: X.astype(np.float32)})[0][0][0]
    return prediction
