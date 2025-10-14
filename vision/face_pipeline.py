from typing import Optional, Tuple
import numpy as np
import face_recognition
from . import db
from .image_utils import compute_face_encoding_from_bgr, encode_image_jpeg

DEFAULT_THRESHOLD = 0.6

def register_face_for_user(usuario_id: int, frame_bgr) -> bool:
    encoding = compute_face_encoding_from_bgr(frame_bgr)
    if encoding is None:
        return False
    img_bytes = encode_image_jpeg(frame_bgr)
    db.insert_face(usuario_id, img_bytes, encoding)
    return True

def recognize_from_frame(frame_bgr) -> Tuple[Optional[int], float]:
    encoding = compute_face_encoding_from_bgr(frame_bgr)
    if encoding is None:
        return (None, 1.0)
    entries = db.list_all_face_encodings()
    if not entries:
        return (None, 1.0)
    user_ids = []
    encs = []
    for uid, enc in entries:
        user_ids.append(uid)
        encs.append(enc)
    encs_np = np.vstack(encs)
    dists = face_recognition.face_distance(encs_np, encoding)
    idx = int(np.argmin(dists))
    best_dist = float(dists[idx])
    best_user = user_ids[idx] if best_dist <= DEFAULT_THRESHOLD else None
    return (best_user, best_dist)
