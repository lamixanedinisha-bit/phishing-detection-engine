# Architecture

## My capstone design (from my presentation decks)

- **Frontend:** React (Vite)
- **Backend:** FastAPI + Python REST API
- **Model:** scikit-learn, TF-IDF (character-level) + lexical URL features;
  Logistic Regression selected after comparing Logistic Regression,
  Naive Bayes and Linear SVM; Pandas / NumPy for data handling
- **Storage:** Supabase PostgreSQL — every scan stored, with scan history
- **Deployment:** Render / Vercel, HTTPS
- **Planning:** Jira, Git / GitHub
- **Reported in the final deck:** 99%+ accuracy — see README.md.
- **Team:** Group 2, team of 6, supervisor Prof. Javad Rezazadeh.
- **My contribution:** project planning, front-end development, testing, research, and the final presentation. Our team of 6 coordinated the work in Jira — dividing tasks, planning sprints and tracking progress.

## This portfolio version (this repo)

Same model family and same API shape, deliberately simplified so it can
be run and reviewed without the original dataset, database or cloud
accounts:

| Capstone | Portfolio version |
| --- | --- |
| React (Vite) frontend | Single static `frontend/index.html`, served by FastAPI |
| TF-IDF + Logistic Regression, trained on a large URL dataset | Same approach, trained at startup on `data/sample_urls.csv` (~120 illustrative URLs) |
| Supabase PostgreSQL scan history | No database — nothing is stored |
| Render / Vercel deployment | Local only (`uvicorn`) |
| Original code | Recreated in this repo from my presentation decks — the original files are no longer accessible after my student email closed |

## Why the model is trained at startup

No model file (`.pkl`) is committed. The training set is small and
text-based, so training on startup is fast (well under a second) and
keeps the repo transparent: anyone can read the exact data the demo
model learned from.
