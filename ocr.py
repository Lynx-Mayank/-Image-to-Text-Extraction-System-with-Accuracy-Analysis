from google.colab import drive
drive.mount('/content/gdrive')

!cp '/content/gdrive/My Drive/TesseractVSEasyOCRVSAWSTextract/data.zip' '/content/data.zip'
!unzip '/content/data.zip' -d '/content/data'

!apt install tesseract-ocr -y
!apt install libtesseract-dev -y

!pip install pytesseract Pillow easyocr boto3

import pytesseract
from PIL import Image
from easyocr import Reader
import boto3
import os

# Initialize EasyOCR
reader = Reader(['en'])

# Optional:
USE_TEXTRACT = False  # Change to True if using AWS Textract
access_key = 'YOUR_AWS_ACCESS_KEY'
secret_access_key = 'YOUR_SECRET_ACCESS_KEY'

if USE_TEXTRACT:
    textract_client = boto3.client(
        'textract',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name='us-east-1'
    )

def read_text_tesseract(image_path):
    try:
        return pytesseract.image_to_string(Image.open(image_path), lang='eng')
    except Exception as e:
        print(f"Tesseract error for {image_path}: {e}")
        return ""

def read_text_easyocr(image_path):
    try:
        results = reader.readtext(Image.open(image_path))
        return ' '.join([result[1] for result in results])
    except Exception as e:
        print(f"EasyOCR error for {image_path}: {e}")
        return ""

def read_text_textract(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            response = textract_client.detect_document_text(Document={'Bytes': image_file.read()})
        return ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])
    except Exception as e:
        print(f"Textract error for {image_path}: {e}")
        return ""

def jaccard_similarity(sentence1, sentence2):
    set1 = set(sentence1.lower().split())
    set2 = set(sentence2.lower().split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0.0

def clean(text):
    return text.lower().replace('\n', '').translate(str.maketrans('', '', '!?."'))

data_dir = '/content/data'
score_tesseract = 0
score_easyocr = 0
score_textract = 0
image_count = 0

for image_file in os.listdir(data_dir):
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(data_dir, image_file)
        ground_truth = os.path.splitext(image_file)[0].replace('_', ' ').lower()

        text_tess = clean(read_text_tesseract(image_path))
        text_easy = clean(read_text_easyocr(image_path))

        score_tesseract += jaccard_similarity(ground_truth, text_tess)
        score_easyocr += jaccard_similarity(ground_truth, text_easy)

        if USE_TEXTRACT:
            text_textract = clean(read_text_textract(image_path))
            score_textract += jaccard_similarity(ground_truth, text_textract)

        image_count += 1

# Printing results
print(f"Images Processed: {image_count}")
if image_count > 0:
    print(f"Score Tesseract: {score_tesseract / image_count:.3f}")
    print(f"Score EasyOCR  : {score_easyocr / image_count:.3f}")
    if USE_TEXTRACT:
        print(f"Score Textract : {score_textract / image_count:.3f}")
else:
    print("No images found to process!")
