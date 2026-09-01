# Z-Gen "Pretty Food" Consumption — Emotional Value & Stickiness

> Submission to the **2026 Zhengda Cup Market Research Competition (正大杯市调大赛)**.
> A multi-method study of how **emotional value** drives Gen-Z's consumption decisions
> and repurchase stickiness for "pretty food" (漂亮饭) in China.

Combining a **531-respondent survey**, **in-depth interviews**, and **Xiaohongshu (RED)
comment text mining**, this project traces the psychological loop behind Gen-Z's
visually-driven dining: consumption → sharing → repurchase.

## Research Question

How does emotional value shape Gen-Z's **consumption frequency** and **repurchase
willingness** for "pretty food"?

## Headline Findings

**Survey (531 valid responses)**

- **Social identity** is the strongest driver of high-frequency consumption
  (standardized β = 0.210, p < 0.01).
- **Emotional comfort** is the decisive factor for repurchase stickiness
  (OR = 1.20, p = 0.005).
- Two distinct personas: **emotion-driven "social sharers"** (79.3%) vs
  **rational "life observers"** (20.7%).
- Reliability α = 0.910, validity KMO = 0.940 — a robust instrument.

**Text mining (255 RED comments)**

- **"好吃" (tasty)** is the top token (32×), with "想吃" (want to eat, 22×),
  "漂亮饭" (10×) and "好看" (good-looking, 6×) rounding out the positive core —
  the "looks good, *and* tastes good" signal dominates.
- 31% of comments are positive and only 6% negative; the rest are neutral
  questions (price / location / shop name). Excluding those, **83% of opinionated
  comments are positive**.

## Methodology

| Component | Description |
|---|---|
| Questionnaire survey | 531 valid responses (488 with consumption experience); mixed online/offline sampling — Changsha core districts + nationwide via social media |
| Pre-survey | 56 valid responses to validate the instrument (α = 0.82, KMO = 0.73) |
| In-depth interviews | Consumers + restaurant operators, framed by TPB and Social Identity Theory |
| Text mining | jieba tokenization + word frequency + rule-based sentiment on RED comments |

### Analysis Pipeline

| Step | Method | Key result |
|---|---|---|
| Reliability | Cronbach's α | 0.910 (9 items) |
| Validity | KMO / Bartlett | 0.940 / χ² = 2181.012 (p < 0.001) |
| Factor analysis | PCA | 5 factors, 76.4% cumulative variance |
| Difference analysis | t-test / ANOVA + Cohen's d | gender, age, occupation, income effects |
| Clustering | K-Means (elbow) | 2 personas (79.3% / 20.7%) |
| Linear regression | OLS | R² = 0.312, social identity strongest |
| Logistic regression | Binary logit | 90% classification accuracy |
| Text mining | word frequency + sentiment | 好吃 32× top; 83% positive (excl. neutral) |

### Theoretical Framework

TPB · Social Identity Theory · Social Currency · SOR · AISAS · PEST.

## Repository Structure

```
Consumer-Research-ZGen/
├── README.md
├── requirements.txt
├── questionnaire.md          # full survey instrument (23 items)
├── data/
│   └── red_comments.csv      # 255 collected RED comments
├── analysis/
│   └── text_mining.py        # tokenize + word frequency + sentiment
├── docs/
│   ├── methodology.md
│   └── findings.md
└── output/                   # generated results (word_frequency.csv, ...)
```

## Getting Started

```bash
# 1. Install dependencies (use a CN mirror if needed)
pip install -r requirements.txt
#   or:  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 2. Run the text-mining pipeline
python analysis/text_mining.py --input data/red_comments.csv --output-dir output
```

Outputs written to `output/`:

- `word_frequency.csv` — top-N tokens by count
- `sentiment_results.csv` — per-comment sentiment label + score
- `summary.json` — aggregate counts and ratios

The sentiment model is a **transparent, rule-based baseline** (a small domain
lexicon + negation handling) rather than a black-box model — extend
`POSITIVE_WORDS` / `NEGATIVE_WORDS` in `text_mining.py` to refine it.

## Reproducibility Note

The competition report cites **74.2% positive sentiment** for the RED corpus.
That figure was computed over a larger comment set with a different method. This
repository ships a smaller, fully reproducible sample (255 comments) and a
transparent baseline, which yields **31% positive / 6% negative / 63% neutral**
(or **83% positive when neutral "price / location" questions are excluded**).
Both numbers tell the same story — sentiment is strongly positive — but the
baseline is deliberately conservative and re-runnable.

## Data & Privacy

- **RED comments are public** user comments collected from Xiaohongshu; the
  crawler itself is intentionally not published (platform ToS + comment privacy).
- **Raw survey responses are not published** — they contain personal attributes
  (gender, age, income, relationship status). Only de-identified aggregates are
  used in `docs/findings.md`.

## Tech Stack

Python · pandas · jieba · openpyxl · SPSS (survey analysis)
