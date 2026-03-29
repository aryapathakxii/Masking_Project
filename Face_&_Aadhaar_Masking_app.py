import streamlit as st
from pdf2image import convert_from_bytes
from ultralytics import YOLO
import pytesseract
import cv2
import numpy as np
import re
from PIL import Image
import io

# ---------------- CONFIG ----------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\poppler\poppler-25.12.0\Library\bin"

model = YOLO(r"D:\AFPL_Project_ML\ML_Interview_Material\yolov8m-face.pt")

# ---------------- YOLO MASKING ----------------
def detect_and_mask_faces_yolo(pages_1):

    processed_images = []

    for i, page in enumerate(pages_1):

        img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        results = model(img)

        faces = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                faces.append((x1, y1, x2-x1, y2-y1))

        print(f"Page {i+1}: {len(faces)} faces detected")

        # ---------- MASKING ----------
        for (x, y, w, h) in faces:

            pad_w = int(0.085 * w)
            pad_h = int(0.085 * h)

            x1 = max(0, x - pad_w)
            y1 = max(0, y - pad_h)
            x2 = min(img.shape[1], x + w + pad_w)
            y2 = min(img.shape[0], y + h + pad_h)

            face = img[y1:y2, x1:x2]

            if face.size == 0:
                continue

            # Clean blur (BEST)
            blurred = cv2.GaussianBlur(face, (99, 99), 40)

            img[y1:y2, x1:x2] = blurred

        processed_images.append(img)

    return processed_images

# ---------------- OCR MASKING ----------------
def mask_aadhaar(img):

    # Improve OCR accuracy (keep simple)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    words = [w.strip() for w in data['text']]
    n = len(words)

    for i in range(n):

        collected = ""
        indices = []

        # 🔥 Flexible grouping (instead of fixed 3 words)
        for j in range(i, min(i + 3, n)):

            word_j = words[j].strip()

            # ❌ Skip words that contain alphabets
            if re.search(r'[A-Za-z]', word_j):
                continue

            clean = re.sub(r'[A-Za-z\s]', '', word_j)
            digits = re.sub(r'\D', '', clean)

            if digits:
                collected += digits
                indices.append(j)

            # Stop once we reach 12 digits
            if len(collected) >= 12:
                break

        # ---------- CASE 1: Any 12-digit (with/without spaces) ----------
        if len(collected) == 12:

            x1 = min(data['left'][k] for k in indices)
            y1 = min(data['top'][k] for k in indices)

            x2 = max(
                data['left'][k] + data['width'][k]
                for k in indices
            )

            y2 = max(
                data['top'][k] + data['height'][k]
                for k in indices
            )

            cv2.rectangle(img, (x1-3, y1-3), (x2+3, y2+3), (0, 0, 0), -1)

        # ---------- CASE 2: Single 12-digit ----------
        word = words[i]
        if re.fullmatch(r"\d{12}", word):

            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]

            cv2.rectangle(img, (x-3, y-3), (x+w+3, y+h+3), (0, 0, 0), -1)

    return img

# ---------------- STREAMLIT UI ----------------
st.set_page_config(
    page_title="PDF_Redaction_Tool",
    page_icon="🚀",
    layout="wide"
)
st.title("PDF Redaction Tool (YOLO + OCR)")
st.image(r"D:\AFPL_Project_ML\ML_Interview_Material\output.png")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:

    if st.button("Process PDF"):

        with st.spinner("Processing..."):

            # PDF → Images
            pages_1 = convert_from_bytes(
                uploaded_file.read(),
                poppler_path=poppler_path
            )

            # YOLO Masking
            processed_images = detect_and_mask_faces_yolo(pages_1)

            # OCR Masking
            final_images = []
            for img in processed_images:
                img = mask_aadhaar(img)
                final_images.append(img)

            # Convert to PIL
            pil_images = []
            for img in final_images:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                pil_images.append(Image.fromarray(img_rgb))

            # Save to memory instead of disk
            pdf_bytes = io.BytesIO()
            pil_images[0].save(
                pdf_bytes,
                format="PDF",
                save_all=True,
                append_images=pil_images[1:]
            )

            st.success("✅ Processing Complete!")

            # DOWNLOAD BUTTON 🔥
            st.download_button(
                label="📥 Download Masked PDF",
                data=pdf_bytes.getvalue(),
                file_name="masked_output.pdf",
                mime="application/pdf"
            )