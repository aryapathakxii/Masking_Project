# 🚀 Overview

This project is a PDF Redaction Tool built using YOLO (Object Detection) and Tesseract OCR. It automatically detects and masks:

👤 Human faces using YOLOv8
🔢 Aadhaar numbers (12-digit sensitive data) using OCR

The tool provides a simple Streamlit web interface where users can upload a PDF and download a redacted version.


# 🏗️ Architecture

<img width="1408" height="768" alt="Project_Architecture" src="https://github.com/user-attachments/assets/070da6b1-742d-494c-b088-dd9b48ca2483" />


# 🧠 How It Works
1. PDF to Images
The uploaded PDF is converted into images using pdf2image (Poppler backend).
2. Face Detection (YOLO)
Uses a pretrained YOLOv8 face detection model.
Detects faces in each page.
Applies Gaussian Blur to hide faces.
3. Text Detection (OCR)
Uses Tesseract OCR to extract text from images.
Detects:
12-digit Aadhaar numbers
Split numbers (e.g., "1234 5678 9012")
4. Masking Sensitive Data
Aadhaar numbers are covered using black rectangles.
5. Output
Processed images are merged back into a masked PDF.
User can download the final output.

# 🛠️ Technologies & Libraries Used
Library	Purpose
streamlit	Web UI
pdf2image	Convert PDF to images
ultralytics	YOLOv8 model for face detection
pytesseract	OCR for text extraction
opencv-python (cv2)	Image processing
numpy	Array operations
Pillow (PIL)	Image handling
re	Regex for Aadhaar detection
io	In-memory file handling

# ⚙️ Installation
1. Install Python Libraries
pip install streamlit pdf2image ultralytics pytesseract opencv-python pillow numpy
2. Install Tesseract OCR
Download from:
https://github.com/UB-Mannheim/tesseract/wiki
Install to:
C:\Program Files\Tesseract-OCR
3. Install Poppler
Download from:
https://github.com/oschwartz10612/poppler-windows/releases
Extract to:
C:\poppler
4. Set Paths in Code
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

poppler_path = r"C:\poppler\Library\bin"

# ▶️ How to Run
python -m streamlit run Face_&_Aadhaar_Masking_app

# 📌 Usage
1. Open the Streamlit app in browser
2. Upload a PDF file
3. Click "Process PDF"
4. Wait for processing
5. Download the masked PDF

# 🔍 Key Features
1. ✅ Face detection & blurring using YOLOv8
2. ✅ Aadhaar number detection using OCR
3. ✅ Handles spaced and continuous digits
4. ✅ Fully automated redaction
5. ✅ Simple UI with download option

# ⚠️ Important Notes
1. Ensure Tesseract & Poppler paths are correct
2. Restart system after setting environment variables
3. Use good quality PDFs for better OCR accuracy
4. Model file path must be correct: model = YOLO("yolov8n-face.pt")

# 🚧 Limitations
1. OCR accuracy depends on image quality
2. May miss partially visible Aadhaar numbers
3. Face detection depends on model performance

# 🔮 Future Improvements
1. Add PAN card / other ID detection
2. Improve OCR accuracy with preprocessing
3. Add multi-language support
4. Deploy as web app

# 👨‍💻 Author
**Arya Pathak**

Developed as part of a Machine Learning project for document redaction and privacy protection.
