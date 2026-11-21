# Phishing Detection Engine

**My Bachelor of IT (Cyber Security) capstone project — Dinisha Lamichhane, Sydney Metropolitan Institute of Technology.**

Portfolio version recreated from my university project work — original files are no longer accessible after my student email closed.

## What it does

A small end-to-end web app that classifies a URL as **benign** or **malicious** in real time, with a confidence score.

- **Backend:** Python, FastAPI, scikit-learn — character-level TF-IDF + Logistic Regression (the model family we selected in the capstone, after comparing Logistic Regression, Naive Bayes and Linear SVM)
- **Frontend:** a single static page (no build step) that calls the API
- **Data:** a small illustrative labelled URL set in `data/sample_urls.csv`

I built this with a team of 6 (Group 2), supervised by Prof. Javad Rezazadeh.

My contribution: project planning, front-end development, testing, research, and the final presentation. Our team of 6 coordinated the work in Jira — dividing tasks, planning sprints and tracking progress.

## Accuracy

My capstone reported **99%+ accuracy** in its final presentation. I state it conservatively as 99%+ because the presentation decks recorded different dataset sizes, so I don't claim a precise figure or a 1.00 test accuracy.

The demo in this repo is trained at startup on the small illustrative dataset in this repo (~120 URLs). It shows how the approach works — its accuracy on that small set is not the capstone result.

## How to run

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

Then open <http://127.0.0.1:8000> — the frontend is served by the API.

Or run the API only and call it directly:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

Expected response (values will vary slightly with the training set):

```json
{
  "url": "https://www.google.com",
  "prediction": "benign",
  "confidence": 0.99,
  "model": "tfidf-char-3-5 + LogisticRegression (portfolio version, illustrative data)"
}
```

## API

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Returns `{"status": "ok", "model_trained": true}` |
| `POST` | `/predict` | Body `{"url": "https://example.com"}` — returns prediction + confidence |
| `GET` | `/` | Serves the demo frontend |

## Architecture

```
User ──> frontend/index.html ──> FastAPI (/predict)
                                        │
                                        ▼
                              TF-IDF (char_wb, 3–5 grams)
                              + Logistic Regression
                                        │
                                        ▼
                              data/sample_urls.csv
                              (illustrative, ~120 URLs,
                               trained at startup — no
                               model file is committed)
```

My capstone also used Supabase PostgreSQL for scan history and Render / Vercel for deployment. This portfolio version deliberately does not include a database or cloud deployment — scan history is not stored. See `docs/ARCHITECTURE.md`.

## Tests

```bash
pip install -r backend/requirements.txt
python -m pytest tests/ -q
```

## Limitations

- Trained on ~120 illustrative URLs, so it will misclassify real-world URLs it has not seen. It is a portfolio demonstration, not a security product.
- No database, no authentication, no rate limiting — do not deploy this as-is for real users.
- No malware, no real phishing URLs, and no link to any live phishing dataset is included.

## About this project

- **My capstone:** Bachelor of Information Technology (Cyber Security), Sydney Metropolitan Institute of Technology, Feb 2024 – Sep 2026 (GPA 5.67 overall). Team of 6, Group 2, supervised by Prof. Javad Rezazadeh.
- **This repo:** a portfolio version I recreated in November 2026, Darwin, from my capstone presentation decks, after my uni student email closed and the original files could no longer be downloaded.

## Licence

MIT — see `LICENSE`.
