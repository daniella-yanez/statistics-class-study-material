"""
ACMS 20340 — Practice Final Exam #2
Flask web application
Run: python app.py
Visit: http://localhost:5000
"""

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ─── Exam Data ────────────────────────────────────────────────────────────────

QUESTIONS = [
    {
        "id": 1,
        "chapter": "Ch. 2 — Descriptive Statistics",
        "text": (
            "A wildlife researcher records the weights (in kg) of 15 grizzly bears:<br><br>"
            "<strong>3.2, 4.1, 4.5, 4.8, 5.0, 5.2, 5.5, 5.7, 6.0, 6.3, 6.5, 6.8, 7.2, 8.1, 22.4</strong><br><br>"
            "Which of the following best describes the appropriate measures of center and spread for this data?"
        ),
        "options": [
            "Mean and standard deviation, because the data is quantitative.",
            "Median and IQR, because the outlier 22.4 makes the data skewed.",
            "Mean and IQR, because IQR is always preferred for spread.",
            "Median and standard deviation, because the median is resistant.",
            "Mean and median together, as both are always needed.",
        ],
        "answer": 1,
        "explanation": (
            "<strong>Answer: B</strong> — When data has outliers or is skewed, the <strong>median and IQR</strong> "
            "are preferred because they are resistant to outliers. The value 22.4 is a suspected outlier "
            "(check: Q₃ + 1.5·IQR), which would strongly pull the mean and inflate the standard deviation."
        ),
    },
    {
        "id": 2,
        "chapter": "Ch. 3 — Correlation",
        "text": (
            "A researcher computes the correlation between height (in inches) and weight (in pounds) "
            "for a sample of adults and gets r = 0.72. If the researcher converts all heights to centimeters "
            "and all weights to kilograms, what will the new correlation be?"
        ),
        "options": [
            "It will decrease, because the units are now smaller.",
            "It will increase, because metric units are more precise.",
            "r = 0.72, because correlation does not change when units are scaled.",
            "r = −0.72, because the direction reverses with metric units.",
            "Cannot be determined without the original data.",
        ],
        "answer": 2,
        "explanation": (
            "<strong>Answer: C</strong> — Correlation r does not change when you change units (scale the data) "
            "or swap the x and y variables. It is a unitless measure of linear association."
        ),
    },
    {
        "id": 3,
        "chapter": "Ch. 4 — Regression",
        "text": (
            "A regression line for predicting a student's exam score (y) from hours studied (x) is "
            "<em>ŷ = 42 + 5.8x</em>. A student studies for 7 hours and scores 83. "
            "What is the residual for this student?"
        ),
        "options": ["−0.6", "+0.6", "−82.6", "+82.6", "0"],
        "answer": 1,
        "explanation": (
            "<strong>Answer: B</strong> — Residual = y − ŷ. First compute ŷ = 42 + 5.8(7) = 82.6. "
            "Then residual = 83 − 82.6 = <strong>+0.6</strong>. The point is <em>above</em> the regression line."
        ),
    },
    {
        "id": 4,
        "chapter": "Ch. 9–10 — Probability",
        "text": (
            "A bag contains 4 red and 6 blue marbles. Two marbles are drawn <em>without replacement</em>. "
            "What is the probability that both marbles drawn are red?"
        ),
        "options": ["0.16", "0.133", "0.40", "0.267", "0.24"],
        "answer": 1,
        "explanation": (
            "<strong>Answer: B</strong> — Without replacement: P(both red) = (4/10) × (3/9) = 12/90 = "
            "<strong>2/15 ≈ 0.133</strong>. Use the General Multiplication Rule since events are not independent."
        ),
    },
    {
        "id": 5,
        "chapter": "Ch. 11 — Normal Distribution",
        "text": (
            "The daily rainfall in a rainforest is Normally distributed with μ = 18 mm and σ = 4 mm. "
            "What is the probability that on a randomly selected day, rainfall exceeds 24 mm?"
        ),
        "options": ["0.9332", "0.1587", "0.0668", "0.8413", "0.3085"],
        "answer": 2,
        "explanation": (
            "<strong>Answer: C</strong> — z = (24 − 18)/4 = 1.5. "
            "P(X > 24) = P(Z > 1.5) = 1 − 0.9332 = <strong>0.0668</strong>."
        ),
    },
    {
        "id": 6,
        "chapter": "Ch. 12 — Binomial Distribution",
        "text": (
            "A factory produces bolts, and 8% of all bolts are defective. A quality inspector randomly "
            "selects 15 bolts. What are the mean and standard deviation of the number of defective bolts?"
        ),
        "options": [
            "μ = 1.2, σ ≈ 1.05",
            "μ = 1.2, σ ≈ 0.11",
            "μ = 0.08, σ ≈ 1.05",
            "μ = 1.38, σ ≈ 1.05",
            "μ = 1.2, σ ≈ 0.074",
        ],
        "answer": 0,
        "explanation": (
            "<strong>Answer: A</strong> — For B(n=15, p=0.08): μ = np = 15(0.08) = <strong>1.2</strong>. "
            "σ = √(np(1−p)) = √(15 × 0.08 × 0.92) = √(1.104) ≈ <strong>1.05</strong>."
        ),
    },
    {
        "id": 7,
        "chapter": "Ch. 13 — Sampling Distributions",
        "text": (
            "The weights of adult male dogs of a certain breed are Normally distributed with μ = 28 kg "
            "and σ = 5 kg. If a random sample of 25 dogs is selected, what is the standard deviation "
            "of the sampling distribution of x̄?"
        ),
        "options": ["5 kg", "0.2 kg", "1.0 kg", "1.12 kg", "25 kg"],
        "answer": 2,
        "explanation": (
            "<strong>Answer: C</strong> — σ/√n = 5/√25 = 5/5 = <strong>1.0 kg</strong>. "
            "This is also called the Standard Error (SE)."
        ),
    },
    {
        "id": 8,
        "chapter": "Ch. 14 — Confidence Intervals",
        "text": (
            "A botanist takes a random sample of 36 plants and finds the sample mean leaf length is 12.4 cm "
            "with σ = 3.0 cm (known). Which of the following is the correct 90% confidence interval "
            "for the population mean leaf length?"
        ),
        "options": [
            "(11.58, 13.22)",
            "(11.42, 13.38)",
            "(11.18, 13.62)",
            "(10.82, 13.98)",
            "(11.65, 13.15)",
        ],
        "answer": 0,
        "explanation": (
            "<strong>Answer: A</strong> — σ known → z-interval. SE = 3/√36 = 0.5. z* = 1.645 for 90% CI. "
            "m = 1.645 × 0.5 = 0.8225. CI: 12.4 ± 0.8225 = <strong>(11.58, 13.22)</strong>."
        ),
    },
    {
        "id": 9,
        "chapter": "Ch. 14–15 — Hypothesis Testing",
        "text": (
            "A pharmaceutical company claims its new drug reduces LDL cholesterol by a mean of μ = 30 points. "
            "A researcher is skeptical and believes the reduction is <em>less</em> than 30 points. "
            "She collects a sample of 50 patients and finds x̄ = 27.5 with σ = 10 (known). What is the P-value?"
        ),
        "options": ["0.0384", "0.0768", "0.9616", "0.0192", "0.4616"],
        "answer": 0,
        "explanation": (
            "<strong>Answer: A</strong> — H₀: μ = 30, Hₐ: μ &lt; 30 (one-sided). "
            "z = (27.5 − 30)/(10/√50) = −1.77. P-value = P(Z ≤ −1.77) ≈ <strong>0.0384</strong>."
        ),
    },
    {
        "id": 10,
        "chapter": "Ch. 15 — Type I & II Errors",
        "text": (
            "A medical researcher tests whether a new vaccine is effective. She sets α = 0.01 (very stringent). "
            "Compared to using α = 0.05, this choice:"
        ),
        "options": [
            "Decreases the probability of a Type I error and increases the probability of a Type II error.",
            "Increases the probability of both Type I and Type II errors.",
            "Increases the probability of a Type I error and decreases the probability of a Type II error.",
            "Has no effect on error probabilities; only sample size matters.",
            "Decreases the probability of both errors.",
        ],
        "answer": 0,
        "explanation": (
            "<strong>Answer: A</strong> — Lowering α reduces P(Type I error), but makes it harder to reject H₀, "
            "which increases P(Type II error) = β and decreases Power = 1 − β. "
            "There is always a tradeoff between Type I and Type II errors for fixed n."
        ),
    },
    {
        "id": 11,
        "chapter": "Ch. 17 — One-Sample t-test",
        "text": (
            "A nutritionist claims the mean daily sugar intake of teenagers is 95 grams. "
            "A random sample of 20 teenagers has x̄ = 102 g and s = 18 g. "
            "The t-statistic for testing H₀: μ = 95 vs. Hₐ: μ ≠ 95 is:"
        ),
        "options": ["t = 1.74", "t = 1.38", "t = 0.39", "t = 7.78", "t = 2.12"],
        "answer": 0,
        "explanation": (
            "<strong>Answer: A</strong> — t = (x̄ − μ₀)/(s/√n) = (102 − 95)/(18/√20) = 7/4.025 ≈ "
            "<strong>1.74</strong>, df = n−1 = 19."
        ),
    },
    {
        "id": 12,
        "chapter": "Ch. 17 — t Robustness",
        "text": (
            "A researcher has a sample of n = 12 measurements that appear to be strongly skewed "
            "with two outliers. Which statement about using a one-sample t-procedure is correct?"
        ),
        "options": [
            "The t-procedure is valid because n ≥ 10.",
            "The t-procedure should NOT be used — with n < 15, data must be close to Normal with no outliers.",
            "The t-procedure is valid because t-distributions are robust to all violations.",
            "The t-procedure is valid because σ is unknown.",
            "The t-procedure is valid if we use df = n.",
        ],
        "answer": 1,
        "explanation": (
            "<strong>Answer: B</strong> — Robustness guidelines: n &lt; 15 requires data to be close to Normal "
            "with NO outliers. With strong skew and two outliers at n = 12, the t-procedure is not appropriate."
        ),
    },
    {
        "id": 13,
        "chapter": "Ch. 18 — Two-Sample t",
        "text": (
            "Researchers compare the mean running speeds (m/s) of two species of lizards using independent "
            "random samples: Species A (n₁ = 12, x̄₁ = 3.8, s₁ = 0.6) and Species B (n₂ = 10, x̄₂ = 3.2, "
            "s₂ = 0.8). The SE for the difference x̄₁ − x̄₂ is approximately:"
        ),
        "options": ["0.297", "0.0882", "0.60", "0.140", "0.529"],
        "answer": 0,
        "explanation": (
            "<strong>Answer: A</strong> — SE = √(s₁²/n₁ + s₂²/n₂) = √(0.36/12 + 0.64/10) = "
            "√(0.094) ≈ <strong>0.297</strong>."
        ),
    },
    {
        "id": 14,
        "chapter": "Ch. 19 — Inference for Proportions",
        "text": (
            "In a survey of 400 randomly selected Notre Dame students, 132 said they exercise at least "
            "5 days per week. Which of the following is the correct 95% large-sample confidence interval "
            "for the population proportion p?"
        ),
        "options": [
            "(0.285, 0.375)",
            "(0.291, 0.369)",
            "(0.274, 0.386)",
            "(0.296, 0.364)",
            "(0.263, 0.397)",
        ],
        "answer": 0,
        "explanation": (
            "<strong>Answer: A</strong> — p̂ = 132/400 = 0.33. SE ≈ 0.02350. "
            "m = 1.96 × 0.02350 = 0.046. CI: 0.33 ± 0.046 ≈ <strong>(0.284, 0.376)</strong>. Closest to A."
        ),
    },
    {
        "id": 15,
        "chapter": "Ch. 19 — Sample Size",
        "text": (
            "A pollster wants to estimate the proportion of voters who support a ballot measure with a margin "
            "of error of no more than 3% at the 95% confidence level. Using the most conservative estimate "
            "for p, what is the minimum required sample size?"
        ),
        "options": ["752", "1068", "1537", "900", "384"],
        "answer": 1,
        "explanation": (
            "<strong>Answer: B</strong> — Use p* = 0.5. n = (1.96/0.03)² × 0.25 ≈ 1067.1 → "
            "round up to <strong>1068</strong>."
        ),
    },
    {
        "id": 16,
        "chapter": "Ch. 20 — Two Proportions",
        "text": (
            "A clinical trial tests a new blood pressure medication. In the treatment group (n₁ = 200), "
            "40 patients experienced side effects (p̂₁ = 0.20). In the control group (n₂ = 200), "
            "60 patients experienced side effects (p̂₂ = 0.30). What is the Absolute Risk Reduction (ARR)?"
        ),
        "options": ["ARR = 0.10", "ARR = 0.33", "ARR = 0.50", "ARR = 0.20", "ARR = 3.0"],
        "answer": 0,
        "explanation": (
            "<strong>Answer: A</strong> — ARR = p̂_control − p̂_treatment = 0.30 − 0.20 = <strong>0.10</strong>. "
            "NNT = 1/ARR = 10. RRR = 0.10/0.30 ≈ 0.33."
        ),
    },
    {
        "id": 17,
        "chapter": "Ch. 21 — Goodness of Fit",
        "text": (
            "An ecologist hypothesizes that four species of birds visit a feeder in equal proportions. "
            "She observes 200 total visits: Species A = 58, B = 46, C = 52, D = 44. "
            "What are the expected count for each species and the degrees of freedom for the chi-square test?"
        ),
        "options": [
            "Expected = 50 for each; df = 4",
            "Expected = 50 for each; df = 3",
            "Expected = 40 for each; df = 3",
            "Expected = 50 for each; df = 199",
            "Expected varies by species; df = 3",
        ],
        "answer": 1,
        "explanation": (
            "<strong>Answer: B</strong> — Uniform hypothesis: expected = 200/4 = <strong>50</strong>. "
            "df = k − 1 = 4 − 1 = <strong>3</strong>."
        ),
    },
    {
        "id": 18,
        "chapter": "Ch. 22 — Chi-Square Two-Way Table",
        "text": (
            "A researcher surveys 300 people about their preferred exercise type and age group:<br><br>"
            "<table class='data-table'>"
            "<tr><th></th><th>Cardio</th><th>Weights</th><th>Yoga</th><th>Total</th></tr>"
            "<tr><td class='rh'>Under 30</td><td>48</td><td>52</td><td>30</td><td>130</td></tr>"
            "<tr><td class='rh'>30 and over</td><td>62</td><td>58</td><td>50</td><td>170</td></tr>"
            "<tr><td class='rh'>Total</td><td>110</td><td>110</td><td>80</td><td>300</td></tr>"
            "</table><br>"
            "What is the expected count of people aged 30 and over who prefer Yoga?"
        ),
        "options": ["45.33", "36.00", "34.67", "50.00", "28.67"],
        "answer": 0,
        "explanation": (
            "<strong>Answer: A</strong> — Expected = (row total × column total) / table total = "
            "(170 × 80) / 300 = <strong>45.33</strong>."
        ),
    },
    {
        "id": 19,
        "chapter": "Ch. 22 — Chi-Square Hypotheses",
        "text": "For the chi-square test of independence in a two-way table, the null hypothesis states:",
        "options": [
            "The row variable causes the column variable.",
            "All expected counts are equal.",
            "There is no association between the row and column variables.",
            "The proportions in each row are equal to 1/c.",
            "Observed counts equal expected counts exactly.",
        ],
        "answer": 2,
        "explanation": (
            "<strong>Answer: C</strong> — H₀: There is no association between the row and column variables. "
            "Hₐ: There IS an association. Note that A is wrong — chi-square tests association, not causation."
        ),
    },
    {
        "id": 20,
        "chapter": "Ch. 24 — One-Way ANOVA",
        "text": (
            "A researcher compares the mean reaction times (ms) of participants across three caffeine conditions "
            "(none, low, high) using ANOVA. The ANOVA table shows MSG = 850 and MSE = 210. "
            "What is the F-statistic, and what are the numerator and denominator degrees of freedom "
            "if there are k = 3 groups and N = 45 total observations?"
        ),
        "options": [
            "F = 4.05; df = (2, 42)",
            "F = 4.05; df = (3, 44)",
            "F = 0.247; df = (2, 42)",
            "F = 4.05; df = (2, 45)",
            "F = 4.29; df = (2, 42)",
        ],
        "answer": 0,
        "explanation": (
            "<strong>Answer: A</strong> — F = MSG/MSE = 850/210 ≈ <strong>4.05</strong>. "
            "Numerator df = k − 1 = 2. Denominator df = N − k = 42. So df = <strong>(2, 42)</strong>."
        ),
    },
    {
        "id": 21,
        "chapter": "Ch. 24 — ANOVA Assumptions",
        "text": (
            "In a one-way ANOVA comparing four groups, the sample standard deviations are "
            "s₁ = 4.2, s₂ = 3.8, s₃ = 7.9, s₄ = 4.5. Is the equal variance assumption satisfied?"
        ),
        "options": [
            "Yes, because all standard deviations are less than 10.",
            "No — the largest s (7.9) is more than 2× the smallest s (3.8).",
            "Yes, because the largest variance (62.4) is less than 4× the smallest variance (14.4).",
            "Cannot be checked without the raw data.",
            "Yes, because the sample sizes are all equal.",
        ],
        "answer": 1,
        "explanation": (
            "<strong>Answer: B</strong> — Rule of thumb: largest sᵢ should be no more than ~2× smallest sᵢ. "
            "Here 7.9/3.8 ≈ 2.08 > 2 and variance ratio = 4.32 > 4. Equal variance assumption is "
            "<strong>NOT</strong> satisfied."
        ),
    },
    {
        "id": 22,
        "chapter": "Ch. 26 — Two-Way ANOVA",
        "text": (
            "In a two-way ANOVA with Factor R (3 levels) and Factor C (2 levels), "
            "what are the degrees of freedom for the interaction term?"
        ),
        "options": ["5", "6", "2", "1", "3"],
        "answer": 2,
        "explanation": (
            "<strong>Answer: C</strong> — Interaction df = (r−1)(c−1) = (3−1)(2−1) = 2 × 1 = <strong>2</strong>. "
            "Main effect df: Factor R = 2; Factor C = 1."
        ),
    },
    {
        "id": 23,
        "chapter": "Ch. 6–7 — Study Design",
        "text": (
            "A university randomly assigns 80 students to either a traditional lecture class or a flipped "
            "classroom model, then measures their final exam scores. This is an example of:"
        ),
        "options": [
            "An observational study using a stratified random sample.",
            "A completely randomized experiment.",
            "A case-control observational study.",
            "A block design experiment.",
            "A cohort observational study.",
        ],
        "answer": 1,
        "explanation": (
            "<strong>Answer: B</strong> — Subjects are randomly assigned to treatment groups. "
            "This is a <strong>completely randomized experiment</strong>, allowing causal conclusions."
        ),
    },
    {
        "id": 24,
        "chapter": "Cumulative — Test Selection",
        "text": (
            "A researcher records whether 150 randomly selected households own a dog (yes/no) and their "
            "annual income category (low/middle/high). She wants to test whether dog ownership is associated "
            "with income level. Which test is most appropriate?"
        ),
        "options": [
            "One-Way ANOVA",
            "Two-sample t-test",
            "Chi-square goodness of fit test",
            "Chi-square test for two-way tables (test for independence)",
            "Two-proportion z-test",
        ],
        "answer": 3,
        "explanation": (
            "<strong>Answer: D</strong> — Both variables are categorical. To test for association between "
            "two categorical variables, use the <strong>chi-square test for two-way tables</strong>. "
            "df = (2−1)(3−1) = 2."
        ),
    },
]

FREE_RESPONSE = [
    {
        "id": 25,
        "chapter": "Ch. 21 — Chi-Square Goodness of Fit",
        "text": (
            "A genetics researcher claims that a particular trait follows a 9:3:3:1 Mendelian ratio "
            "across four phenotypes (A, B, C, D). In an experiment with 160 offspring, the observed counts are:"
            "<br><br>"
            "<table class='data-table' style='max-width:500px;'>"
            "<tr><th>Phenotype</th><th>A</th><th>B</th><th>C</th><th>D</th><th>Total</th></tr>"
            "<tr><td class='rh'>Observed</td><td>92</td><td>28</td><td>26</td><td>14</td><td>160</td></tr>"
            "</table><br>"
            "Test whether the observed data are consistent with the 9:3:3:1 ratio at α = 0.05."
        ),
        "parts": [
            {
                "label": "Part A — State the hypotheses.",
                "solution": (
                    "<strong>H₀:</strong> The phenotype proportions follow a 9:3:3:1 ratio "
                    "(p_A = 9/16, p_B = 3/16, p_C = 3/16, p_D = 1/16).<br>"
                    "<strong>Hₐ:</strong> At least one of the proportions differs from the hypothesized value."
                ),
            },
            {
                "label": "Part B — Calculate the expected counts. Check conditions.",
                "solution": (
                    "Expected counts = n × pᵢ₀:<br>"
                    "E_A = 160 × (9/16) = <code>90</code>&emsp;"
                    "E_B = 160 × (3/16) = <code>30</code>&emsp;"
                    "E_C = 160 × (3/16) = <code>30</code>&emsp;"
                    "E_D = 160 × (1/16) = <code>10</code><br><br>"
                    "<strong>Conditions:</strong> (1) SRS ✓; (2) All expected counts ≥ 1: min = 10 ✓; "
                    "(3) No more than 20% of expected counts &lt; 5: 0 out of 4 ✓. All conditions met."
                ),
            },
            {
                "label": "Part C — Calculate the χ² statistic, find the P-value, and state your conclusion.",
                "solution": (
                    "χ² = (92−90)²/90 + (28−30)²/30 + (26−30)²/30 + (14−10)²/10<br>"
                    "= 0.044 + 0.133 + 0.533 + 1.600 = <code>2.311</code><br><br>"
                    "df = k − 1 = 3. Using Table D: P-value &gt; 0.25.<br><br>"
                    "<strong>Conclusion:</strong> Since P-value &gt; 0.05, we <strong>fail to reject H₀</strong>. "
                    "The data are consistent with the 9:3:3:1 Mendelian ratio."
                ),
            },
        ],
    },
    {
        "id": 26,
        "chapter": "Ch. 24 — One-Way ANOVA",
        "text": (
            "A food scientist tests whether mean moisture content (%) differs among three types of crackers. "
            "Random samples are taken and summarized below:<br><br>"
            "<table class='data-table' style='max-width:460px;'>"
            "<tr><th>Cracker Type</th><th>n</th><th>x̄</th><th>s</th></tr>"
            "<tr><td class='rh'>Whole Wheat</td><td>8</td><td>12.4</td><td>1.8</td></tr>"
            "<tr><td class='rh'>Sourdough</td><td>8</td><td>14.1</td><td>2.2</td></tr>"
            "<tr><td class='rh'>Rye</td><td>8</td><td>13.0</td><td>1.6</td></tr>"
            "</table><br>"
            "Overall mean x̄ = 13.17. Test at α = 0.05."
        ),
        "parts": [
            {
                "label": "Part A — State the hypotheses and check the equal variance assumption.",
                "solution": (
                    "<strong>H₀:</strong> μ₁ = μ₂ = μ₃ &emsp; "
                    "<strong>Hₐ:</strong> Not all means are equal.<br><br>"
                    "<strong>Equal variance check:</strong> Largest s = 2.2, Smallest s = 1.6. "
                    "Ratio = 2.2/1.6 = 1.375 &lt; 2 ✓. Assumption is satisfied."
                ),
            },
            {
                "label": "Part B — Calculate MSG and MSE.",
                "solution": (
                    "<strong>MSG</strong> = Σnᵢ(x̄ᵢ − x̄)² / (k−1) = "
                    "[8(0.5929) + 8(0.8649) + 8(0.0289)] / 2 = 11.893/2 = <code>5.947</code><br><br>"
                    "<strong>MSE</strong> = Σ(nᵢ−1)sᵢ² / (N−k) = "
                    "[7(3.24) + 7(4.84) + 7(2.56)] / 21 = 74.48/21 = <code>3.547</code>"
                ),
            },
            {
                "label": "Part C — Calculate F, find the P-value, and state a conclusion.",
                "solution": (
                    "F = MSG/MSE = 5.947/3.547 = <code>1.677</code>, df = (2, 21).<br><br>"
                    "P-value &gt; 0.10 (F is well below F₀.₁₀ ≈ 2.57 for df 2,21).<br><br>"
                    "<strong>Conclusion:</strong> Since P-value &gt; 0.05, we <strong>fail to reject H₀</strong>. "
                    "There is not sufficient evidence that mean moisture content differs among the three types."
                ),
            },
        ],
    },
    {
        "id": 27,
        "chapter": "Ch. 17–18 — Matched Pairs & Interpretation",
        "text": (
            "A physical therapist measures patients' pain scores (0–10) before and after a new treatment. "
            "Data for 7 patients:<br><br>"
            "<table class='data-table'>"
            "<tr><th>Patient</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th></tr>"
            "<tr><td class='rh'>Before</td><td>7</td><td>8</td><td>6</td><td>9</td><td>5</td><td>7</td><td>8</td></tr>"
            "<tr><td class='rh'>After</td><td>4</td><td>5</td><td>5</td><td>6</td><td>3</td><td>4</td><td>6</td></tr>"
            "<tr><td class='rh'>Difference</td><td>3</td><td>3</td><td>1</td><td>3</td><td>2</td><td>3</td><td>2</td></tr>"
            "</table><br>"
            "The mean difference is x̄_diff = 2.43 and s_diff = 0.787."
        ),
        "parts": [
            {
                "label": "Part A — Why is a matched pairs design appropriate? State the hypotheses.",
                "solution": (
                    "<strong>Why matched pairs:</strong> The same 7 patients are measured twice. "
                    "The two measurements are paired — not independent samples. "
                    "This controls for individual differences in baseline pain levels.<br><br>"
                    "<strong>H₀:</strong> μ_diff = 0 (no effect)<br>"
                    "<strong>Hₐ:</strong> μ_diff &gt; 0 (treatment reduces pain)"
                ),
            },
            {
                "label": "Part B — Carry out the t-test at α = 0.05. Calculate t, find the P-value, and conclude.",
                "solution": (
                    "t = (x̄_diff − 0) / (s_diff/√n) = 2.43 / (0.787/√7) = 2.43 / 0.2974 = <code>8.17</code>, df = 6.<br><br>"
                    "From Table C with df = 6, one-sided: t = 8.17 >> t₀.₀₀₀₅ = 5.959 → "
                    "<strong>P-value &lt; 0.0005</strong>.<br><br>"
                    "<strong>Conclusion:</strong> Since P-value &lt; 0.05, we <strong>reject H₀</strong>. "
                    "The data provide very strong evidence that the treatment reduces pain scores "
                    "(mean reduction ≈ 2.43 points)."
                ),
            },
        ],
    },
]


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html",
                           questions=QUESTIONS,
                           free_response=FREE_RESPONSE)


@app.route("/api/check", methods=["POST"])
def check_answer():
    """Check a multiple-choice answer and return correctness + explanation."""
    data = request.get_json()
    qid      = int(data.get("id", 0))
    selected = int(data.get("selected", -1))

    question = next((q for q in QUESTIONS if q["id"] == qid), None)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    correct = question["answer"]
    return jsonify({
        "correct":     selected == correct,
        "correct_idx": correct,
        "explanation": question["explanation"],
    })


@app.route("/api/questions")
def get_questions():
    """Return all MC questions as JSON (for potential SPA use)."""
    return jsonify(QUESTIONS)


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
