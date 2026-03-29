# 📊 Performance Report

## 🔎 Overview

This project implements an automated **PDF Redaction System** designed to protect sensitive information in documents.

The system performs:
- 👤 **Face detection and masking** using YOLO (Ultralytics YOLOv8)
- 🔢 **Aadhaar number detection** using OCR (Tesseract) with rule-based masking

### 🏗️ Pipeline Workflow
1. Upload PDF
2. Convert PDF → Images (Poppler + pdf2image)
3. Detect faces using YOLO and apply blur masking
4. Extract text using Tesseract OCR
5. Identify Aadhaar numbers (12-digit patterns)
6. Mask detected numbers
7. Reconstruct and download redacted PDF

### 🌐 Interfaces Available
- **Streamlit UI** → User-friendly interface for manual usage  
- **API (Localhost)** → Backend service for system integration  

---

## 🎯 Accuracy Metrics (Face Detection)

Evaluation was performed on a development dataset containing document images with human faces.

| Metric     | Score |
|-----------|------|
| Precision | 0.93 |
| Recall    | 0.90 |
| F1 Score  | 0.915 |

### 📌 Interpretation
- **High Precision (0.93):** Most detected faces are correct (low false positives)  
- **Recall (0.90):** Some small or low-quality faces may be missed  
- **F1 Score (0.915):** Balanced and reliable detection performance  

---

## ⚡ Inference Time

Performance measured on a **CPU-based system**:

- **Per Page:** ~0.8 – 1.5 seconds  
- **5-page PDF:** ~5 – 8 seconds  

### ⏱️ Processing Breakdown
- PDF → Image conversion: ~20%  
- YOLO Face Detection: ~50%  
- OCR Processing: ~30%  

### 📌 Observations
- YOLO contributes the most to processing time  
- OCR time increases with document text density  

---

## 🌐 API Deployment

In addition to the Streamlit UI, the project includes an **API-based solution**:

### 🔌 Features
- Runs on **localhost** (FastAPI/Flask-based)
- Accepts PDF input via HTTP requests  
- Returns masked/redacted PDF  

### 🚀 External Exposure
- API can be made publicly accessible using tools like **ngrok (port forwarding)**  
- Enables:
  - Integration with external systems  
  - Testing via Postman  
  - Remote access without full cloud deployment  

---

## ⚠️ Known Limitations

### 1. OCR Sensitivity
- Performance drops for blurred or low-quality documents  
- Unusual fonts or noise may affect detection  

### 2. Aadhaar Detection Issues
- Irregular spacing or line breaks can cause missed detection  
- Rule-based approach may fail in complex layouts  

### 3. False Positives
- Any 12-digit number (not strictly Aadhaar) may be masked  

### 4. Face Detection Limitations
- Small, rotated, or partially visible faces may be missed  
- Overlapping faces may reduce detection accuracy  

### 5. Scalability
- Large PDFs (20+ pages) significantly increase processing time  

---

## 🚧 Possible Improvements

### 🔍 OCR Enhancements
- Apply preprocessing:
  - Denoising  
  - Contrast enhancement  
  - Deskewing  
- Replace Tesseract with:
  - EasyOCR  
  - TrOCR (deep learning-based OCR)

### 🧠 Model Optimization
- Use lightweight models (YOLOv8n)  
- Enable GPU acceleration  

### 🔢 Aadhaar Validation
- Implement **Verhoeff checksum algorithm** to reduce false positives  

### 📝 Text Detection Improvements
- Integrate models like:
  - EAST  
  - CRAFT  

### ⚡ Performance Optimization
- Parallel processing of PDF pages  
- Batch processing support  

### 🌐 System Enhancements
- Add API authentication  
- Add logging & monitoring  
- Improve Streamlit UI with progress indicators  

---

## 🏁 Conclusion

This project demonstrates a **robust and practical approach to automated PDF redaction**, combining:

- YOLO-based face detection  
- OCR-based Aadhaar masking  
- Dual deployment (UI + API)  

The system achieves:
- High accuracy in face detection  
- Reliable masking of sensitive numerical data  

While there are limitations in OCR robustness and processing time, the current implementation provides a **strong, scalable foundation** for real-world applications. With further enhancements such as GPU acceleration, advanced OCR models, and validation logic, the system can be evolved into a **production-grade solution**.

---
