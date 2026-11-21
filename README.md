# Phishing Detection Engine — Rebuilt Portfolio Version

> **Rebuilt portfolio version, recreated from the capstone presentation — original uni code is no longer accessible (student email closed).**
>
> This is **not** the original submitted code. The original Bachelor of IT (Cyber Security) capstone was built by a team of 6 at Sydney Metropolitan Institute of Technology, supervised by Prof. Javad Rezazadeh. Dinisha Lamichhane was a member of that team; her individual contribution is **[to confirm]** — do not assume a specific part from this repo alone.
>
> Unit code is also **[to confirm]**: the Drive files are labelled ICT312 / ICT313, while a transcript check flagged ICT310 / ICT311 for the capstone.

## What it does

A small end-to-end web app that classifies a URL as **benign** or **malicious** in real time, with a confidence score.

- **Backend:** Python, FastAPI, scikit-learn — character-level TF-IDF + Logistic Regression (the model family selected in the original capstone, after comparing Logistic Regression, Naive Bayes and Linear SVM)
- **Frontend:** a single static page (no build step) that calls the API
- **Data:** a small illustrative labelled URL set in `data/sample_urls.csv` — **not** the original capstone dataset

## Accuracy — read this first

The original capstone presentation reported **"99%+ accuracy reported"**. The exact final figures are **not confirmed** here: the decks in Drive disagree on the dataset size (126,502 vs 632,508 URLs), and a 1.00 test-accuracy figure was reported in one deck. **Do not quote 1.00 test accuracy as fact.**

This rebuilt version is trained at startup on the small illustrative dataset in this repo (~120 URLs). It is a working demonstration of the approach, not a reproduction of the capstone result. Its accuracy on that small set is not the capstone result.

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
  "model": "tfidf-char-3-5 + LogisticRegression (rebuilt, illustrative data)"
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

The original capstone also used Supabase PostgreSQL for scan history and Render / Vercel for deployment. This rebuilt version deliberately **does not** include a database or cloud deployment — scan history is not stored. See `docs/ARCHITECTURE.md` for the original design vs this rebuild.

## Tests

```bash
pip install -r backend/requirements.txt
python -m pytest tests/ -q
```

## Limitations

- Trained on ~120 illustrative URLs, so it will misclassify real-world URLs it has not seen. It is a portfolio demonstration, not a security product.
- No database, no authentication, no rate limiting — do not deploy this as-is for real users.
- No malware, no real phishing URLs, and no link to any live phishing dataset is included.
- The original dataset, the original code, and the completed capstone final report were not in the Drive folder that was available to rebuild from.

## Project history

- **Original:** Bachelor of IT (Cyber Security) capstone, Sydney Metropolitan Institute of Technology, Feb 2024 – Sep 2026 (Dinisha Lamichhane, GPA 5.67 overall). Team of 6, Group 2.
- **Rebuilt:** November 2026, Darwin, from the capstone presentation decks in Google Drive, after the uni student email closed and the original code could no longer be downloaded.

## Licence

MIT — see `LICENSE`.
