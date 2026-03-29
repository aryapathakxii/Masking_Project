# ML Engineer Assessment: Document PII Detection & Masking Pipeline

**Assessment Duration:** 7 calendar days
**Issued By:** Engineering Hiring Team
**Difficulty Level:** Intermediate to Advanced

---

## Background

Government identity programs like Aadhaar generate and process millions of documents containing sensitive Personally Identifiable Information (PII) - including photographs, unique identification numbers, addresses, and biometric references. These documents often exist as multi-page PDFs with mixed content: narrative text, tabular data, human photographs, and non-human images (facilities, equipment, vehicles, etc.).

When such documents are shared, stored, or audited, the PII within them must be automatically detected and redacted to comply with data protection regulations. This requires a robust ML pipeline capable of:

1. **Detecting human faces** across varying image sizes, positions, and layouts within a PDF
2. **Identifying sensitive numeric patterns** (e.g., 12-digit Aadhaar-format numbers) using OCR
3. **Masking/redacting** detected PII while preserving the rest of the document

---

## Your Task

Build an **end-to-end ML pipeline** that accepts a PDF document as input and produces a redacted PDF as output, with all human faces masked and (optionally) all Aadhaar-format numbers redacted.

### Input

You are provided with:

- **`development_set.pdf`** — A 9-page compliance report containing a mix of human face photographs, non-human images (infrastructure, vehicles, animals, equipment), and text with embedded Aadhaar-format numbers. Use this for development, experimentation, and validation.

- **`test_set.pdf`** — A 16-page audit report designed for rigorous evaluation. This document contains intentionally challenging scenarios that your pipeline must handle. **Your final submission must include the processed output of this file.**

### Output

A redacted version of the input PDF where:

1. **All human faces are masked** — Faces should be obscured (blurred, pixelated, or covered with a solid overlay). The masking must completely conceal the identity while being visually clear that redaction occurred.

2. **All Aadhaar-format numbers are redacted** — 12-digit numbers in the format `XXXX XXXX XXXX` appearing in the document text should be detected via OCR and redacted (replaced with `XXXX XXXX XXXX` or blacked out).

3. **Non-human images must NOT be masked** — Images of objects, animals, vehicles, infrastructure, etc. must remain untouched. False positives (masking non-human content) will count against your score.

4. **Document integrity is preserved** — The output PDF should retain its original structure, text, layout, and non-PII content as closely as possible.

---

## Constraints & Guidelines

- **No restrictions** on programming language, ML framework, pre-trained models, cloud services, or third-party APIs. Use whatever tools best solve the problem.
- You may use pre-trained models or train/fine-tune your own. Justify your choice.
- The pipeline should be **reproducible** — another engineer should be able to run it from scratch using your documentation.
- Prioritize **recall over precision** for face detection (missing a face is worse than a false positive on an edge case), but excessive false positives will be penalized.
- The solution should handle PDFs of **arbitrary length and layout** — not be hardcoded to the specific test file.

---

## Challenges You Should Expect

The test PDF includes several intentional challenges:

| Challenge | Description |
|-----------|-------------|
| **Size variation** | Faces appear at sizes ranging from tiny thumbnails (~ 0.6 inch) to near-full-page (~ 4.2 inch) |
| **Position variation** | Images are left-aligned, right-aligned, centered, in grids, at page corners, and embedded in tables |
| **Density variation** | Some pages have 6+ images, others have none. One page has only text with Aadhaar numbers |
| **Mixed content** | Human faces appear alongside non-human images at similar sizes (discrimination test) |
| **Animal faces** | Cat and dog images (which have faces) are present — your detector must distinguish human from animal |
| **Low-light images** | Non-human images are from low-light/dark conditions, adding visual complexity |
| **OCR complexity** | Aadhaar-format numbers appear in body text, tables, and alongside images |

---

## Deliverables

Your submission **must** include the following:

### 1. Source Code Repository
- All source code in a **Git repository** (GitHub/GitLab/Bitbucket)
- Clean, well-organized code with meaningful commit history
- A comprehensive **README.md** with:
  - Setup instructions (dependencies, environment)
  - How to run the pipeline
  - Architecture overview
  - Model/approach choices and rationale

### 2. Processed PDFs
- Redacted output of **`development_set.pdf`**
- Redacted output of **`test_set.pdf`**
- Both files should be included in the repository or submitted alongside it

### 3. Deployable Service
- A **containerized API** (Docker preferred) that accepts a PDF file and returns the redacted version
- Endpoint specification:
  - `POST /redact` — accepts a PDF file, returns the redacted PDF
  - `GET /health` — returns service status
- Include a `Dockerfile` and `docker-compose.yml` (if applicable)
- The service should start with a single command (e.g., `docker-compose up`)

### 4. Performance Report
- A brief document (1-2 pages) covering:
  - **Accuracy metrics** on the development set (precision, recall, F1 for face detection)
  - **Inference time** (time to process each PDF)
  - **Known limitations** and failure cases
  - **Possible improvements** with more time/resources

### 5. Solution Development Journal *(Important)*
- Fill in the provided **`SOLUTION_JOURNAL.md`** template throughout the week
- This is **not optional** — we use it to evaluate your problem-solving process, not just the final output
- Document your decisions, trade-offs, and learnings

---

## Evaluation Criteria

Your submission will be evaluated on the following dimensions (see `EVALUATION_RUBRIC.md` for detailed scoring):

| Dimension | Weight | What We Look For |
|-----------|--------|------------------|
| **Face Detection Accuracy** | 30% | Precision, recall, F1 on test set. Handling of varying sizes/positions. False positive rate. |
| **Solution Architecture** | 20% | Clean code, modularity, separation of concerns, appropriate abstractions, error handling. |
| **Deployment Readiness** | 20% | Working Docker container, API design, documentation, reproducibility. |
| **OCR & Number Masking** | 15% | Aadhaar number detection accuracy, handling of different text layouts and formats. |
| **Problem-Solving Process** | 15% | Quality of the Solution Journal, iterative approach, thoughtful trade-offs. |

---

## Submission Instructions

1. Push your complete solution to a **Git repository** and share the link
2. Ensure the repository contains all deliverables listed above
3. The repository's README should enable us to reproduce your results within 15 minutes
4. Submit by **(EMAIL RECEIVED DATE + 7) days, 11:59 PM IST**

---

## FAQ

**Q: Can I use cloud-based APIs (AWS Rekognition, Google Vision, Azure Face API)?**
A: Yes, but you must also demonstrate the ability to run a local/self-hosted model. Cloud APIs can be used for comparison or as a fallback.

**Q: What if I can't complete the Docker/API part?**
A: Submit what you have. A working script with good detection accuracy is better than a perfect API with poor detection. However, deployment readiness is 20% of the score.

**Q: Should I train a model from scratch?**
A: Not necessarily. Using pre-trained models with appropriate fine-tuning or configuration is perfectly acceptable — and often the pragmatic choice. We want to see good engineering judgment.

**Q: How should I handle pages with no images?**
A: Your pipeline should handle them gracefully — no errors, no false detections, output should match input.

**Q: What format should the masked faces be in?**
A: Any visually clear redaction method is acceptable: solid black/colored rectangle, Gaussian blur, pixelation, or hatching pattern. The key is that the face must be completely unrecognizable.

---

*Good luck. We look forward to seeing your approach.*
