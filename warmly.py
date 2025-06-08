from typing import Dict, Literal
import requests
from ast import literal_eval
from flask import Flask, Response, request, jsonify
from flask_cors import CORS

GEMINI_WEBSITE: str = "https://gemini-wrapper-nine.vercel.app/gemini"
PROMPT: str = \
"""
You will be given a transcript of a conversation between multiple people. Your task is to analyze the conversation and extract key
structured information into the following categories: Names of Speakers – List all unique participants. Topics Discussed – Provide
a bullet point summary of major themes or subjects. Social or Business Overlaps – Identify shared interests, professional connections,
organizations, or mutual experiences between participants. Things to Follow Up On – List unresolved questions, tasks, or opportunities
that require further attention. Action Items & Owners – For any discussed tasks, specify what needs to be done and who (if anyone)
committed to it. Dates or Deadlines Mentioned – Extract any time-related references. Please structure your output in a JSON format
using different keys for each of the categories mentioned above and keep the writing concise but informative. If you do not have a
valid transcript, output an empty JSON object. Here is the transcript:
{transcript}
"""

app: Flask = Flask(__name__)
app.debug = False
CORS(app)

@app.route("/")
def hello() -> Literal["Hello."]:
    return "Hello."

@app.route("/structured_transcript", methods=["POST"])
def parse() -> Response:
    data: Dict[str, str] = request.get_json(force=True)
    if "transcript" not in data:
        raise ValueError("'transcript' key not found in input JSON.")

    json_data: Dict = {
        "prompt": PROMPT.format(transcript=data["transcript"])
    }
    response: requests.Response = requests.post(GEMINI_WEBSITE, json=json_data)
    output: str = response.json()["output"]
    output = output \
        .replace("```json", "") \
        .replace("```", "")
    output_dict: Dict = literal_eval(output)
    return jsonify(output_dict)