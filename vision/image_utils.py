from typing import Optional
import cv2
import numpy as np
import face_recognition

def bgr_to_rgb(image_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

def encode_image_jpeg(image_bgr: np.ndarray, quality: int = 90) -> bytes:
    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    ok, buf = cv2.imencode(".jpg", image_bgr, encode_params)
    if not ok:
        raise RuntimeError("Falha ao codificar imagem JPEG")
    return buf.tobytes()

def decode_image_jpeg(jpeg_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(jpeg_bytes, dtype=np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise RuntimeError("Falha ao decodificar imagem JPEG")
    return image

def compute_face_encoding_from_bgr(image_bgr: np.ndarray) -> Optional[np.ndarray]:
    image_rgb = bgr_to_rgb(image_bgr)
    boxes = face_recognition.face_locations(image_rgb, model="hog")
    if not boxes:
        return None
    encs = face_recognition.face_encodings(image_rgb, known_face_locations=boxes)
    if not encs:
        return None
    return encs[0]
