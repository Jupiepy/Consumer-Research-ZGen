# Key Findings

## 1. The instrument is reliable and valid

- Cronbach's α = **0.910** (9 core items), well above the 0.7 threshold.
- KMO = **0.940**, Bartlett's χ² = 2181.012 (p < 0.001) — the data are strongly
  suited to factor analysis.

## 2. Five latent factors explain 76.4% of variance

PCA extracted five factors: social-aesthetic, curiosity-relaxation, service,
price, and utility (76.4% cumulative variance). Emotional-value items load
highest on the first factors, confirming the four-dimension structure.

## 3. Consumers split into two personas

K-Means clustering (elbow method) yields two stable segments:

| Persona | Share | Profile |
|---|---|---|
| 情绪驱动型 "社交分享达人" | **79.3%** | high emotional value, share-oriented, driven by aesthetics & social identity |
| 理性务实型 "生活观察者" | **20.7%** | price/utility-driven, low sharing behavior |

## 4. Social identity drives frequency; emotional comfort drives stickiness

- **Linear regression** (emotional-value dimensions → consumption frequency):
  R² = 0.312; **social identity is the strongest predictor (β = 0.210, p < 0.01)**.
- **Binary logistic regression** (dimensions → repurchase willingness):
  90% classification accuracy; **emotional comfort has the largest effect
  (OR = 1.20, p = 0.005)**, followed by aesthetic expression (OR = 1.177) and
  social identity (OR = 1.155).

Interpretation: **getting people to eat "pretty food" often is about social
belonging; getting them to come *back* is about emotional comfort.**

## 5. Difference analysis

t-tests and ANOVA (with Cohen's d) show significant differences in emotional-value
sensitivity across gender, age, occupation and income — younger, student, and
higher-frequency consumers score higher on social-aesthetic dimensions.

## 6. Text mining confirms a positive but "value-for-money" gap

On the RED comment sample (`analysis/text_mining.py`, 255 comments):

- **"好吃"** is the top token (32×), with "想吃" (22×), "漂亮饭" (10×) and
  "好看" (6×) forming the positive core.
- Sentiment: **31% positive, 6% negative, 63% neutral** (mostly price/location
  questions). Excluding neutral questions, **83% of opinionated comments are
  positive**.
- The recurring pain points are **price ("贵" / "多少钱" / "价格侠")** and the
  **"looks good but doesn't taste good"** risk — matching the survey's "价格贵 /
  不好吃" first-impression items.

> The competition report cites 74.2% positive sentiment over a larger corpus with
> a different method; see the Reproducibility Note in `README.md`. Directionally
> the two agree — sentiment is strongly positive.
