from flask import Flask, jsonify, request
import html2text
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
API_KEY = os.getenv("OPEN_AI_KEY")

class Recipe(BaseModel):
  recipe_name: str
  author: str
  ingredients: list[str]
  instructions: list[str]

def convert(url: str) -> str:
  h = html2text.HTML2Text()
  h.ignore_links = True
  h.ignore_images = True

  r = requests.get(url)
  return h.handle(r.text)

def extract_recipe(markdown: str) -> str:
  
  client = OpenAI(api_key=API_KEY)

  response = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
      {
        "role": "system",
        "content": "You are given recipe information in markdown format and need to extract the key componenets consisting of the following: recipe name, recipe author, ingredients, and instrcutions"
      },
      { 
        "role": "user", 
        "content": markdown
      }
    ],
    response_format=Recipe,
    temperature=0.5,
    max_tokens=16383,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

  return response.choices[0].message.content

app = Flask(__name__)

@app.route('/api/simplify', methods=['POST'])
def simplify():
  data = request.get_json()
  url = data['url']
  markdown = convert(url)
  recipe = extract_recipe(markdown)

  request_data = {"original": markdown,"converted": recipe}

  return jsonify(request_data)
