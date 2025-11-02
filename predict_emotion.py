import numpy as np
import cv2
<<<<<<< HEAD
import os

# Suppress TensorFlow warnings and info messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0 = all messages, 1 = no info, 2 = no warnings, 3 = errors only

try:
    from tensorflow.keras.models import load_model
except ImportError:
    print("Warning: TensorFlow not available. Emotion detection will not work.")
    load_model = None
=======
from tensorflow.keras.models import load_model
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a

# Emotion classes
emotion_classes = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

<<<<<<< HEAD
# Global model variable to cache the loaded model
_emotion_model = None

def _load_model():
    """Load the emotion model (cached after first load)"""
    global _emotion_model
    if _emotion_model is not None:
        return _emotion_model
    
    if load_model is None:
        raise ImportError("TensorFlow is not installed")
    
    import os
    # Get the base directory path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'fer_model.h5')
    
    # Check if model file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    
    try:
        _emotion_model = load_model(model_path, compile=False)
        return _emotion_model
    except Exception as e:
        raise RuntimeError(f"Error loading model: {str(e)}")

=======
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
def predict_emotion_from_image(image_bytes):
    """
    Predict emotion from image bytes using FER model.

    Args:
        image_bytes: Raw image data from Django POST request.

    Returns:
        str: Predicted emotion label or error message.
    """
    try:
<<<<<<< HEAD
        # Load model (cached after first load)
        model = _load_model()
=======
        # Load the pre-trained model (load inside function to avoid global load issues)
        model = load_model('fer_model.h5')
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
        # Decode image bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return 'Decode_Error'

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            return 'No_Face_Detected'

<<<<<<< HEAD
        # Select the largest face if multiple faces detected
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        (x, y, w, h) = largest_face

        # Extract face ROI with some padding
        padding = 10
        x_start = max(0, x - padding)
        y_start = max(0, y - padding)
        x_end = min(gray.shape[1], x + w + padding)
        y_end = min(gray.shape[0], y + h + padding)
        
        face_roi = gray[y_start:y_end, x_start:x_end]

        # Resize to 48x48 (FER models typically use 48x48)
        face_roi = cv2.resize(face_roi, (48, 48), interpolation=cv2.INTER_AREA)

        # Apply histogram equalization for better contrast
        face_roi = cv2.equalizeHist(face_roi)

        # Normalize pixel values to 0.0-1.0
        face_roi = face_roi.astype('float32') / 255.0
        
        # Ensure values are in [0, 1] range
        face_roi = np.clip(face_roi, 0.0, 1.0)
=======
        # Assume the first face detected
        (x, y, w, h) = faces[0]

        # Extract face ROI
        face_roi = gray[y:y+h, x:x+w]

        # Resize to 48x48
        face_roi = cv2.resize(face_roi, (48, 48))

        # Normalize pixel values to 0.0-1.0
        face_roi = face_roi.astype('float32') / 255.0
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a

        # Reshape to Keras input format (1, 48, 48, 1)
        face_roi = np.expand_dims(face_roi, axis=[0, -1])

<<<<<<< HEAD
        # Ensure shape is correct
        if len(face_roi.shape) != 4 or face_roi.shape != (1, 48, 48, 1):
            # Fix shape if needed
            face_roi = face_roi.reshape((1, 48, 48, 1))

        # Predict emotion (verbose=0 to suppress output)
        predictions = model.predict(face_roi, verbose=0)
        
        # Handle different prediction output shapes
        if predictions.ndim > 1:
            # Get the first prediction if it's a batch
            pred_scores = predictions[0] if len(predictions.shape) > 1 else predictions
        else:
            pred_scores = predictions
        
        # Convert to numpy array if not already
        if not isinstance(pred_scores, np.ndarray):
            pred_scores = np.array(pred_scores)
        
        # Flatten to 1D if needed
        pred_scores = pred_scores.flatten()
        
        # Apply softmax if values don't sum to ~1.0 (model might output logits)
        if pred_scores.sum() > 1.5 or pred_scores.sum() < 0.5:
            # Apply softmax normalization
            exp_scores = np.exp(pred_scores - np.max(pred_scores))  # Subtract max for numerical stability
            pred_scores = exp_scores / exp_scores.sum()
        
        # Debug: Print prediction scores occasionally (every 20th prediction to see what's happening)
        import random
        debug_print = random.random() < 0.05  # 5% of the time
        if debug_print:
            print(f"Raw predictions shape: {predictions.shape}")
            print(f"Prediction scores: {pred_scores}")
            print(f"Scores sum: {pred_scores.sum():.3f}")
            print(f"All emotion scores: {dict(zip(emotion_classes, pred_scores))}")
            print(f"Predicted class index: {np.argmax(pred_scores)}")
        
        # Get the class with highest probability
        predicted_class = int(np.argmax(pred_scores))
        
        # Verify class index is valid
        if predicted_class >= len(emotion_classes) or predicted_class < 0:
            if debug_print:
                print(f"Warning: Invalid class index {predicted_class}, defaulting to Neutral")
            predicted_class = 6  # Neutral
        
        # Get confidence score (convert to float)
        try:
            confidence = float(pred_scores[predicted_class]) if isinstance(pred_scores, np.ndarray) else float(pred_scores)
        except (IndexError, TypeError):
            confidence = 0.5  # Default confidence
        
        if debug_print:
            print(f"Selected emotion: {emotion_classes[predicted_class]}, Confidence: {confidence:.3f}")
        
        predicted_emotion = emotion_classes[predicted_class]
        
        # If confidence is extremely low, return Neutral instead
        # But be less strict - only if confidence is very low
        if confidence < 0.15:
            predicted_emotion = 'Neutral'
        
        return predicted_emotion

    except Exception as e:
        import traceback
        # Log the error for debugging
        error_msg = f"Error in predict_emotion_from_image: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # This will show in Django console
=======
        # Predict emotion
        predictions = model.predict(face_roi)
        predicted_class = np.argmax(predictions, axis=1)[0]
        predicted_emotion = emotion_classes[predicted_class]

        return predicted_emotion

    except Exception as e:
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
        return 'Decode_Error'
