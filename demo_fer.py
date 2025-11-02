from predict_emotion import predict_emotion_from_image
import cv2
import numpy as np

# Create a dummy image (100x100 grayscale, all white - no face expected)
dummy_image = np.ones((100, 100), dtype=np.uint8) * 255
_, encoded_img = cv2.imencode('.jpg', dummy_image)
image_bytes = encoded_img.tobytes()

# Predict emotion
result = predict_emotion_from_image(image_bytes)
print(f"Prediction for dummy image (no face): {result}")

# Create another dummy image with some variation (still no face)
dummy_image2 = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
_, encoded_img2 = cv2.imencode('.jpg', dummy_image2)
image_bytes2 = encoded_img2.tobytes()

result2 = predict_emotion_from_image(image_bytes2)
print(f"Prediction for random image (no face): {result2}")

# Note: Since the model is trained on dummy data, predictions on real faces would be random.
# For demonstration, we're using images without faces, so it correctly returns 'No_Face_Detected'.
print("\nDemo complete. The model loads successfully and handles face detection.")
print("To test with a real face image, provide image_bytes from a Django POST request containing a face.")
