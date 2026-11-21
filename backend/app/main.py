"""Phishing Detection Engine — rebuilt portfolio version.

Trains a TF-IDF (character n-gram) + Logistic Regression classifier at
startup on the small illustrative labelled set in data/sample_urls.csv.

This is a rebuild from the capstone presentation, NOT the original
submitted code. See README.md for the accuracy and provenance warnings.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "sample_urls.csv"
FRONTEND_DIR = BASE_DIR / "frontend"

MODEL_NAME = "tfidf-char-3-5 + LogisticRegression (rebuilt, illustrative data)"


def load_training_data(path: Path = DATA_PATH):
    urls, labels = [], []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            urls.append(row["url"].strip())
            labels.append(row["label"].strip().lower())
    if len(set(labels)) < 2:
        raise ValueError("training data must contain both benign and malicious examples")
    return urls, labels


def build_model() -> Pipeline:
    urls, labels = load_training_data()
    model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="char_wb", ngram_range=(3, 5), max_features=5000
                ),
            ),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    model.fit(urls, labels)
    return model


model = build_model()

app = FastAPI(
    title="Phishing Detection Engine (rebuilt portfolio version)",
    description=(
        "Classifies a URL as benign or malicious. "
        "Rebuilt from the capstone presentation; trained on a small "
        "illustrative dataset. Not the original submitted code."
    ),
)


class PredictRequest(BaseModel):
    url: HttpUrl


class PredictResponse(BaseModel):
    url: str
    prediction: str
    confidence: float
    model: str


@app.get("/health")
def health():
    return {"status": "ok", "model_trained": True}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    url = str(req.url)
    proba = model.predict_proba([url])[0]
    classes = list(model.classes_)
    idx = int(proba.argmax())
    return PredictResponse(
        url=url,
        prediction=classes[idx],
        confidence=round(float(proba[idx]), 4),
        model=MODEL_NAME,
    )


if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(FRONTEND_DIR / "index.html")
