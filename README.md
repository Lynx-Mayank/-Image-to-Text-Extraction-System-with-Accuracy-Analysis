# Text Detection System

This project is a Python-based OCR (Optical Character Recognition) benchmarking system developed in Google Colab. It extracts text from images using multiple OCR engines — Tesseract, EasyOCR, and optionally AWS Textract — and compares their accuracy using Jaccard similarity.

---

## Features

- Supports three OCR engines:
  - 🧾 Tesseract (open-source)
  - 🧠 EasyOCR (deep learning-based)
  - ☁️ AWS Textract (cloud-based, optional)
- Compares OCR output with ground truth derived from image filenames
- Calculates Jaccard similarity score for performance evaluation
- Works directly in Google Colab using Google Drive for storage
- Exception handling for robust image processing

---

## Folder & File Structure

My Drive/
└── TesseractVSEasyOCRVSAWSTextract/
└── data.zip # Zip file containing all input images

Each image should be named with its ground truth text using underscores (e.g., `hello_world.png` → ground truth: "hello world").

---

## Technologies Used

- Python
- Google Colab
- Tesseract OCR (`pytesseract`)
- EasyOCR
- AWS Textract (optional)
- Pillow (`PIL`)
- Google Drive for data access
- Jaccard Similarity for evaluation

---

## Installation & Setup done in Colab

