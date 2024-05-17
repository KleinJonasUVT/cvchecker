import os
import pymysql
import pandas as pd
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import fitz
import requests
import base64

def get_gpt_response(file):
    doc = fitz.open(file)
    pages = len(doc)
    image_list = []
    for i in range(pages):
        page = doc.load_page(i)
        pixmap = page.get_pixmap()
        img = pixmap.tobytes()
        image_list.append(img)

    # OpenAI API Key
    api_key = os.getenv("OPENAI_API_KEY")

    def convert_image_to_base64(image_bytes):
        return base64.b64encode(image_bytes).decode('utf-8')

    # Convert images to base64
    base64_images = [convert_image_to_base64(img) for img in image_list]

    # Initialize the messages list
    content = [
        {
            "type": "text",
            "text": "How to improve this resume?"
        }
    ]

    # Append the image URLs to the messages list
    for base64_image in base64_images:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })

    # Example API endpoint and headers (replace with the actual endpoint and headers)
    api_endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "system",
        "content": "You are a CV reviewer that provides feedback on a resume. \
            Provide feedback on 1. the resume's content, 2. the resume's format, and 3. the resume's overall effectiveness.\
            structure you feedback like html tags; for example, <h2>Content Feedback</h2> <p>The content of the resume is strong...</p>.\
            Do not include ```html at the beginning and ``` at the end."
        },
        {
        "role": "user",
        "content": content
        }
    ]
    }

    response = requests.post(api_endpoint, headers=headers, json=payload)
    answer = response.json()["choices"][0]["message"]["content"]

    return answer