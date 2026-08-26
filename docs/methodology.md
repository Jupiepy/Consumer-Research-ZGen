# Methodology

## Research Design

A mixed-methods study triangulating three data sources:

1. **Questionnaire survey** — the primary quantitative source.
2. **In-depth interviews** — consumers and "pretty food" operators, used to
   refine the instrument and interpret results.
3. **Web text mining** — public Xiaohongshu (RED) comments, used to validate and
   enrich the survey findings with real-world language.

## Timeline

| Phase | Period | Activity |
|---|---|---|
| Preparation | 2025-10-10 → 11-15 | literature review, topic selection, field observation |
| Pre-survey | 2025-11-16 → 11-25 | pilot questionnaire (64 distributed → 56 valid) |
| Instrument revision | 2025-11-26 → 12-15 | wording, layout, and item refinement from pilot feedback |
| Formal survey | 2025-12-16 → 2026-01-03 | stratified online + offline distribution → 531 valid |
| Field follow-up | 2026-01-04 → 01-15 | merchant interviews, on-site observation |
| Analysis & writing | 2026-01-16 → 03 | SPSS + Python analysis, report |

## Sampling

- **Pre-survey:** convenience sampling among students (online platform + in-class),
  64 distributed, 56 valid (82.35% valid rate).
- **Formal survey:** stratified sampling with quotas by region (Changsha districts),
  status (student / employed) and consumption frequency; online (问卷星, RED,
  campus communities) + offline (business districts, university town) combined.

## Measurement

The core scale uses 9 five-point Likert items spanning four emotional-value
dimensions (视觉审美 / 社交认同 / 压力缓解 / 新奇体验) plus control variables
(price, quality, service, peer influence, media push). See `questionnaire.md`.

## Analysis Methods

**Survey (SPSS)**

- Descriptive statistics
- Reliability — Cronbach's α
- Validity — KMO + Bartlett's test, exploratory factor analysis (PCA)
- Difference analysis — independent t-test, one-way ANOVA, Cohen's d
- Clustering — K-Means (elbow method)
- Linear regression — emotional-value dimensions → consumption frequency
- Binary logistic regression — dimensions → repurchase willingness

**Text mining (Python, `analysis/text_mining.py`)**

1. Clean comments (strip @mentions, URLs, emoji, RED shortcodes).
2. Tokenize with jieba (custom domain dictionary + stopwords).
3. Word-frequency analysis.
4. Rule-based sentiment: a small transparent lexicon with negation handling
   produces a signed score per comment, classified positive / negative / neutral.

## Theoretical Framework

Theory of Planned Behavior (TPB) · Social Identity Theory · Social Currency ·
SOR model · AISAS model · PEST.
