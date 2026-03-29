from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import StreamingResponse
from pdf2image import convert_from_bytes
from ultralytics import YOLO
import pytesseract
import cv2
import numpy as np
import re
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor
import torch

# -----------------------------
# FastAPI instance
# -----------------------------
app = FastAPI(title="Masking API Optimized GPU/CPU")

# -----------------------------
# API KEY
# -----------------------------
API_KEY = "mysecret12122000"
def verify_key(key):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# -----------------------------
# Paths for Windows
# -----------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\poppler-25.12.0\Library\bin"
MODEL_PATH = r"D:\Arya_User\Masking_Project\API\yolov8n-face.pt"

# -----------------------------
# Load YOLO model
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO(MODEL_PATH)  # let YOLO handle device automatically
if device == "cuda":
    model.to("cuda")

# -----------------------------
# PDF conversion (all pages at once)
# -----------------------------
def convert_pdf(pdf_bytes, dpi=200):
    pages = convert_from_bytes(pdf_bytes, dpi=dpi, poppler_path=POPPLER_PATH)
    if not pages:
        raise HTTPException(status_code=500, detail="PDF conversion failed")
    return pages

# -----------------------------
# YOLO face detection + blur (batch)
# -----------------------------
def detect_and_mask_faces(pages):
    images = [cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR) for p in pages]

    # Use batch inference if GPU
    results = model(images, device=device, verbose=False)

    processed_images = []
    for img, r in zip(images, results):
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2-x1, y2-y1
            pad_w, pad_h = int(0.085*w), int(0.085*h)
            x1, y1 = max(0,x1-pad_w), max(0,y1-pad_h)
            x2, y2 = min(img.shape[1], x2+pad_w), min(img.shape[0], y2+pad_h)
            face = img[y1:y2, x1:x2]
            if face.size==0: continue
            img[y1:y2, x1:x2] = cv2.GaussianBlur(face,(99,99),40)
        processed_images.append(img)
    return processed_images

# -----------------------------
# OCR masking
# -----------------------------
def mask_aadhaar(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)[1]
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
    words = [w.strip() for w in data['text']]
    n = len(words)

    for i in range(n):
        collected = ""
        indices = []
        for j in range(i, min(i+3, n)):
            word_j = words[j].strip()
            if re.search(r'[A-Za-z]', word_j):
                continue
            digits = re.sub(r'\D','', re.sub(r'[A-Za-z\s]','', word_j))
            if digits:
                collected += digits
                indices.append(j)
            if len(collected) >= 12:
                break
        if len(collected)==12:
            x1 = min(data['left'][k] for k in indices)
            y1 = min(data['top'][k] for k in indices)
            x2 = max(data['left'][k]+data['width'][k] for k in indices)
            y2 = max(data['top'][k]+data['height'][k] for k in indices)
            cv2.rectangle(img,(x1-3,y1-3),(x2+3,y2+3),(0,0,0),-1)
        word = words[i]
        if re.fullmatch(r"\d{12}", word):
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            cv2.rectangle(img,(x-3,y-3),(x+w+3,y+h+3),(0,0,0),-1)
    return img

def process_ocr_parallel(images):
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(mask_aadhaar, images))

# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def home():
    return {"status":"API is running"}

# -----------------------------
# Main API endpoint
# -----------------------------
@app.post("/mask-pdf")
async def mask_pdf(file: UploadFile=File(...), x_api_key: str=Header(None)):
    try:
        verify_key(x_api_key)
        pdf_bytes = await file.read()
        pages = convert_pdf(pdf_bytes)
        yolo_images = detect_and_mask_faces(pages)
        final_images = process_ocr_parallel(yolo_images)
        pil_images = [Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) for img in final_images]

        output = io.BytesIO()
        pil_images[0].save(output, format="PDF", save_all=True, append_images=pil_images[1:])
        output.seek(0)
        return StreamingResponse(output, media_type="application/pdf")
    except Exception as e:
        print("🔥 ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
