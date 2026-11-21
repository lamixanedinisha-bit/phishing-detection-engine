# Architecture — original capstone vs this rebuild

## Original capstone (from the presentation decks in Drive)

- **Frontend:** React (Vite)
- **Backend:** FastAPI + Python REST API
- **Model:** scikit-learn, TF-IDF (character-level) + lexical URL features;
  Logistic Regression selected after comparing Logistic Regression,
  Naive Bayes and Linear SVM; Pandas / NumPy for data handling
- **Storage:** Supabase PostgreSQL — every scan stored, with scan history
- **Deployment:** Render / Vercel, HTTPS
- **Planning:** Jira, Git / GitHub
- **Reported in the final deck:** "99%+ accuracy reported" — see README.md.
  The exact final dataset / metrics are **not confirmed** (decks disagree:
  126,502 vs 632,508 URLs). Do not quote a 1.00 test accuracy as fact.
- **Team:** Group 2, team of 6, supervisor Prof. Javad Rezazadeh.
  Dinisha Lamichhane's individual contribution: **[to confirm]**.
- **Unit code:** **[to confirm]** — ICT312 / ICT313 in the Drive files,
  ICT310 / ICT311 flagged in a transcript check.

## This rebuild (this repo)

Same model family and same API shape, deliberately simplified so it can
be run and reviewed without the original dataset, database or cloud
accounts:

| Original | Rebuild |
| --- | --- |
| React (Vite) frontend | Single static `frontend/index.html`, served by FastAPI |
| TF-IDF + Logistic Regression, trained on a large URL dataset | Same approach, trained at startup on `data/sample_urls.csv` (~120 illustrative URLs) |
| Supabase PostgreSQL scan history | No database — nothing is stored |
| Render / Vercel deployment | Local only (`uvicorn`) |
| Original code | **Not included** — it could not be downloaded after the uni student email closed |

## Why the model is trained at startup

No model file (`.pkl`) is committed. The training set is small and
text-based, so training on startup is fast (well under a second) and
keeps the repo transparent: anyone can read the exact data the demo
model learned from.
