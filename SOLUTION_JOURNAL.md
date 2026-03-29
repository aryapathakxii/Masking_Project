# Solution Development Journal

**Candidate Name:** Arya Pathak
**Date Started:** 26th March 2026
**Date Submitted:** 29th March 2026
---

> **Instructions:** Fill in this journal as you work through the assessment over the week. This is NOT meant to be polished documentation — we want to see your raw thought process, experiments, and decision-making. Write entries as you go, not retroactively. Honest accounts of dead ends and failures are valued more than a perfect narrative.

---

## Day 1: Problem Analysis & Initial Research

### Problem Understanding
*What is the core problem? What are the key challenges you identified after reading the problem statement and examining the PDFs?*
The primary objective is to accurately mask human faces and Aadhaar numbers within the provided documents. The key challenges include:

**Facial Recognition Complexity:** The system must distinguish human faces from animal images and other objects. Technical hurdles include low-light conditions (poor brightness and contrast), partial occlusions (half-faces), and small scale due to subjects being far from the lens.

**Aadhaar Number Extraction:** Identifying the 12-digit Aadhaar number is complicated by inconsistent formatting, such as irregular spacing, varying font sizes, and line breaks. Additionally, some numbers are embedded within complex tabular structures, requiring robust detection before masking.

### Initial Observations
*What did you notice when examining the development PDF? (Image sizes, positions, text patterns, edge cases, etc.)*
Upon reviewing the development PDFs, several critical observations were made regarding image quality, layout, and data patterns:

**Image Quality and Variability:** Many images suffer from low brightness and poor contrast, which may hinder feature extraction. I also observed significant scale variation; some faces are extremely small due to the subject’s distance from the camera, while others are partial or "half-face" views where the subject is not looking directly at the lens.

**Object Noise:** The documents are not limited to human subjects. They contain animals and miscellaneous objects that could trigger false positives for facial recognition, necessitating a more robust filtering layer.

**Text Patterns (Aadhaar):** The 12-digit Aadhaar numbers do not follow a uniform format. Key inconsistencies include:

**Irregular Spacing:** Some digits are bunched together while others have extra spaces.

**Layout Issues:** Numbers are frequently split across new lines or embedded within complex tabular structures.

**Typography:** Variations in font size and style make simple pattern matching difficult.

**Positional Challenges:** Aadhaar numbers and faces are not found in fixed coordinates; their positions shift depending on the document type, requiring a dynamic detection approach rather than a static template.

### Approach Brainstorming
*List 2-3 possible approaches you're considering. What are the pros/cons of each?*

| Approach              | Pros                                                   | Cons                                                                      |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------- |
| OpenCV (CV2)          | Easy to apply Gaussian blur or masking                 | Poor performance on low-light images, partial faces; high false positives |
| YOLO (v8n-face)       | High accuracy for human faces; fast inference with GPU | Requires GPU for large PDFs; model size matters                           |
| Tesseract OCR + Regex | Can detect Aadhaar numbers dynamically                 | OCR errors on small/dim digits; regex fails if spacing is irregular       |


### Resources Identified
*Papers, libraries, pre-trained models, or tutorials you plan to use.*
1. YOLOv8n-face.pt — pre-trained model for face detection
2. Tesseract OCR — text detection and Aadhaar extraction
3. Libraries: pdf2image, opencv-python, Pillow, numpy, FastAPI
4. Tutorials and GitHub examples for PDF redaction pipelines.


## Day 2: Environment Setup & Data Exploration

### Environment & Stack
*What tools, libraries, and frameworks did you set up? Any version issues or compatibility problems?*
1. YOLOv8n-face.pt — pre-trained model for face detection
2. Tesseract OCR — text detection and Aadhaar extraction
3. Libraries: pdf2image, opencv-python, Pillow, numpy, FastAPI
4. Tutorials and GitHub examples for PDF redaction pipelines

No version issues or any compatibility problem by far

Notes:

1. Poppler required for pdf2image.
2. Initial installation of YOLO model on local machine worked; Render required adjustments for GPU-less environment.

### PDF Exploration
*How did you approach extracting content from the PDFs? What library/method did you use for PDF parsing? What challenges did you encounter?*
1. Used pdf2image.convert_from_bytes to convert PDFs to images.
2. Observed: Multi-page PDFs could exceed memory limits.
3. Approach: chunk pages in batches to reduce memory usage.


### Key Findings
*What did you learn about the data that influences your approach?*
1. PDF pages may contain multiple faces per page.
2. Text OCR is error-prone for low-resolution or dimly scanned PDFs.
3. Some PDFs exceeded 50 pages, requiring batched processing for efficiency.


## Day 3: Model Selection & Initial Experiments

### Models Evaluated
*Which face detection models did you try? Report initial results.*

| Model                | Faces Detected (Dev Set) | False Positives | Inference Time | Notes                                          |
| -------------------- | ------------------------ | --------------- | -------------- | ---------------------------------------------- |
| YOLOv8m-face         | 14/15                    | 1               | ~0.5s/page     | Good for frontal faces                         |
| YOLOv12n-face        | 15/15                    | 0-1             | ~0.3s/page     | Faster and smaller, better for multi-page PDFs |
| OpenCV Haar Cascades | 12/15                    | 3+              | ~0.2s/page     | Too many false positives on objects            |


### Chosen Approach
*Which model/approach did you select and why?*
Chosen Approach
1. YOLOv8n-face for face detection
2. Tesseract OCR + Regex for Aadhaar number detection
3. Chunking strategy for multi-page PDFs to reduce memory usage if required


### Initial Results on Development Set
*What were your first end-to-end results? What worked? What didn't?*

1. PDF Processing
1.1 Successfully converted uploaded PDF documents into individual pages and then into images using Poppler with pdf2image.
1.2 ✅ Worked well: Fast and reliable conversion for most PDFs.
2. Initial Face Detection Attempt (OpenCV)
2.1 Tried using OpenCV (cv2 Haar Cascades) for human face detection and masking.
2.2 ❌ Did not work well:
2.2.1 Low accuracy
2.2.2 Failed in detecting faces with different angles, lighting, or low resolution
2.2.3 High false positives and missed detections
3. Improved Face Detection (YOLOv8)
3.1 Switched to YOLOv8 face detection model for better performance.
3.2 ✅ Worked well:
3.2.1 Accurate face detection across different orientations
3.2.2 Better generalization on real-world documents
3.3 Used OpenCV (cv2) for:
3.3.1 Image manipulation
3.3.2 Applying Gaussian blur masking
4. Text Detection & Aadhaar Masking (OCR)
4.1 Integrated Tesseract OCR to extract text from images.
4.2 Implemented regex-based logic to detect:
4.2.1 Continuous 12-digit numbers
4.2.2 Spaced Aadhaar numbers (e.g., XXXX XXXX XXXX)
4.5 ✅ Worked moderately well: Successfully masked most Aadhaar numbers
4.6 ⚠️ Limitations:
4.6.1 OCR accuracy depends heavily on image quality
4.6.2 Some digits may be missed in noisy or low-resolution scans


## Day 4: Pipeline Development

### Architecture Decisions
*How did you structure your pipeline? What are the main components?*

```
PDF (multi-page) 
    ↓
pdf2image → List of Images (pages)
    ↓
Chunk pages → Batch processing
    ↓
YOLO face detection → Blur/mask faces
    ↓
OCR + Regex → Mask Aadhaar numbers
    ↓
Pillow → Combine images → PDF
    ↓
Output masked PDF
```

### Integration Challenges
*What was hard about connecting the pieces together? (PDF parsing -> image extraction -> detection -> masking -> PDF reconstruction)*
1. Converting PDFs → Images → Masked Images → PDF without losing resolution.
2. Tesseract sometimes misread digits, requiring regex grouping logic.
3. Large PDFs caused memory spikes; solved by processing in chunks.


### Configuration & Parameters
*What parameters does your pipeline expose? How did you choose default values?*
1. Converting PDFs → Images → Masked Images → PDF without losing resolution.
2. Tesseract sometimes misread digits, requiring regex grouping logic.
3, Large PDFs caused memory spikes; solved by processing in chunks.


## Day 5: Testing & Iteration

### Development Set Results

| Metric                              | Value                                |
| ----------------------------------- | ------------------------------------ |
| Faces detected (out of 15)          | 14–15                                |
| False positives                     | 0–1                                  |
| Aadhaar numbers detected (out of 9) | 8–9                                  |
| Processing time                     | ~1 min for 50 pages on local 8GB RAM |


### Issues Found & Fixes
*What problems did you discover during testing? How did you fix them?*

| Issue                      | Root Cause                     | Fix Applied                                         |
| -------------------------- | ------------------------------ | --------------------------------------------------- |
| OCR missed digits          | Low contrast or small font     | Preprocess images: grayscale + thresholding         |
| Memory spike               | Processing all pages at once   | Chunk pages into batches                            |
| False positives on objects | YOLO detects non-human objects | Switched to YOLOv12n, filtered small bounding boxes |


### Edge Cases Handled
*Which edge cases did you specifically address?*
1. Half-faces and small faces
2. Split Aadhaar numbers across lines or tables
3. Low-resolution scanned pages


## Day 6: Deployment & API Development

### Containerization
*How did you containerize the solution? Any challenges with Docker (image size, dependencies, GPU support)?*
1. Docker used to containerize the API.
2. Challenges: Large model size (>50MB), dependencies (opencv, poppler, pytesseract).
3. Solution: Pre-uploaded yolov8n-face.pt in repo; used Docker to install minimal dependencies only.
4. Tested Docker but it's required docker installation on the local machine so instead deployed it without docker and used port forwarding using ngrok for making API live.


### API Design
*Describe your API endpoints, request/response format, and error handling.*
1. Endpoint: /mask-pdf
2. Method: POST
3. Headers: x-api-key for authentication
4. Request: multipart/form-data PDF file upload
5. Response: Masked PDF (application/pdf)
6. Error Handling: Returns HTTP 401 if API key invalid, HTTP 500 for processing errors

### Testing the Deployed Service
*Did you test the API end-to-end? What was the experience?*
1. Tested with PDFs of 1 page, 10 pages and 18 pages.
2. Works on local machine in <1 min
3. Chunking ensures API can handle multi-page PDFs without memory crash


## Day 7: Final Testing, Documentation & Polish

### Test Set Results
| Metric                               | Value                           |
| ------------------------------------ | ------------------------------- |
| Faces detected (out of 26)           | 25–26                           |
| False positives                      | 0–1                             |
| Aadhaar numbers detected (out of 23) | 21–23                           |
| Processing time                      | < 1 min per 50-page PDF (local) |


### Known Limitations
*What doesn't work well? What would break your pipeline?*
1. Extremely low-resolution PDFs may cause OCR misses.
2. Partial/occluded faces may occasionally not be masked.
3. Serverless APIs with limited runtime (like Render free tier) cannot process 50-page PDFs efficiently.
4. Also app deployment is extremely slow at CPU so tried deploying over GPU which is costly for Assessment purpose. So Instead deployed app on local machine.


### What I'd Do Differently
*With hindsight, what would you change about your approach? What would you do with more time?*
1. Use GPU-enabled Hugging Face Spaces, Colab and Render for faster inference on large PDFs but it's costly
2. Integrate parallel OCR processing to reduce runtime further
3. Train YOLO on additional augmented face dataset to reduce false negatives


### Final Reflections
*What did you learn? What was the hardest part? What are you most proud of?*
1. Learned the end-to-end pipeline of PDF redaction
2. Most challenging: OCR and chunking for large PDFs
3. Most proud of: Achieving accurate face and Aadhaar masking with multi-page support


## Appendix: Experiment Log (Optional)

*Use this section to log any additional experiments, benchmarks, or notes that don't fit in the daily entries.*
| Date  | Experiment                    | Result                         | Decision                                 |
| ----- | ----------------------------- | ------------------------------ | ---------------------------------------- |
| Day 1 | YOLOv8m-face vs YOLOv8n-face  | v8n slightly faster & smaller  | Choose YOLOv8n                           |
| Day 1 | Process all pages at once     | Memory spike                   | Implemented batch chunking               |
| Day 2 | OCR preprocessing             | Improved Aadhaar detection     | Used thresholding + grouping logic       |
| Day 2 | Render API deployment         | 502 / 500 errors               | Pre-uploaded model, reduced dependencies |


*Thank you for documenting your journey. This journal is a critical part of our evaluation — it tells us how you think, not just what you build.*
