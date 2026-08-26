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

- **Social identity** is the strongest driver of high-frequency consumption
  (standardized β = 0.210, p < 0.01).
- **Emotional comfort** is the decisive factor for repurchase stickiness
  (OR = 1.20, p = 0.005).
- Two distinct personas: **emotion-driven "social sharers"** (79.3%) vs
  **rational "life observers"** (20.7%).
- 74.2% of RED comments are positive, but "tastes bad" and "expensive" polarize
  opinion — the **"looks good, doesn't taste good"** gap is the #1 pain point.

## Methodology

| Component | Description |
|---|---|
| Questionnaire survey | 531 valid responses (488 with consumption experience); mixed online/offline sampling — Changsha core districts + nationwide via social media |
| Pre-survey | 56 valid responses to validate the instrument (α = 0.82, KMO = 0.73) |
| In-depth interviews | Consumers + restaurant operators, framed by TPB and Social Identity Theory |
| Text mining | Python crawler + tokenization + sentiment analysis on Xiaohongshu posts/comments |

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
| Text mining | word freq + sentiment | 74.2% positive, "tasty/tasteless" polarization |

### Theoretical Framework
TPB · Social Identity Theory · Social Currency · SOR · AISAS · PEST.

## Repository Structure

```
Consumer-Research-ZGen/
├── README.md
├── questionnaire.md        # full survey instrument (23 items)
├── report.pdf              # full report (optional)
├── data/                   # anonymized survey + RED comments
├── analysis/
│   ├── text_mining.py      # crawler + word frequency + sentiment
│   └── stats/              # SPSS syntax / Python stats scripts
└── docs/
    ├── methodology.md
    └── findings.md
```

## Data & Privacy

Raw survey responses contain personal attributes (gender, age, income, relationship
status) and are **not published**. Only de-identified or aggregated data is shared.

## Tech Stack

Python · pandas · jieba (tokenization) · sentiment analysis · SPSS
