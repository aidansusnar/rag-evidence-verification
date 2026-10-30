# Evaluation Protocol — Financial RAG Evidence Verification

**Project:** Evaluating Evidence Verification in Financial Retrieval-Augmented Generation (RAG)  
**Version:** 0.1 — Proposed Protocol  
**Date:** October 29, 2026  
**Status:** Draft — to be finalized before experimental runs

## 1. Purpose and Research Question

This protocol defines how the baseline and evidence-verified RAG systems will be evaluated using FinanceBench financial questions and corporate annual reports.

**Research question:** Does an additional evidence-verification step improve the correctness and evidential support of financial RAG answers, and are those improvements worth the additional latency, token usage, and API cost?

The evaluation will measure both answer quality and computational efficiency. All scoring rules should be established before reviewing experimental results to reduce the risk of changing criteria to favor either system.

## 2. Experimental Setup

### 2.1 Dataset

The initial experiment will use a 12-question subset of the FinanceBench open-source benchmark.

| Company | Source Document | Questions |
|---|---|---:|
| Advanced Micro Devices (AMD) | 2022 Form 10-K | 7 |
| PepsiCo | 2022 Form 10-K | 5 |
| **Total** | **2 financial reports** | **12** |

The source documents and FinanceBench JSONL file are stored locally under `data/` and excluded from Git tracking.

The 12-question subset is the initial pilot. Expansion to approximately 20 questions may be considered if time and resources permit.

### 2.2 Experimental Conditions

**Condition A — Baseline RAG**

1. Receive a financial question.
2. Retrieve relevant passages from the associated annual report.
3. Provide the question and retrieved passages to the hosted language model.
4. Generate an answer using the supplied evidence.
5. Record the answer, retrieved passage identifiers, timing, and token usage.

**Condition B — Evidence-Verified RAG**

1. Reuse the same question, retrieved passages, and initial answer from Condition A.
2. Submit the initial answer and retrieved evidence to an additional verification step.
3. Evaluate whether the answer is supported by the retrieved passages.
4. Produce one of three outcomes:
   - **Accept:** Preserve the initial answer.
   - **Revise:** Correct the answer using only the available evidence.
   - **Abstain:** Decline to provide a substantive answer when the available evidence is insufficient.
5. Record the final answer, verification decision, timing, and token usage.

The verification condition must not receive additional gold evidence, benchmark answers, or privileged information unavailable to the baseline.

Only one verification pass is permitted in the initial experiment. Revision occurs within that pass; there is no iterative verification loop.

### 2.3 Controlled Variables

To make the comparison fair, both conditions will use:

- Identical evaluation questions.
- Identical retrieved passages and passage ordering.
- The same initial generated answer.
- The same source-document version.
- Fixed retrieval settings, including the embedding model, chunking configuration, and top-k value.
- Recorded LLM model identifiers and generation settings.

The baseline answer will be generated once per question and reused for the verification condition.

The verifier's prompt and role necessarily differ from the baseline generation prompt because the verifier performs a different task.

The experiment measures the effect of adding verification to a fixed baseline pipeline, not the effect of changing the retrieval system.

## 3. Answer Correctness

### 3.1 Definition

Answer correctness measures whether a system's final answer accurately addresses the financial question when compared with the FinanceBench reference answer and supporting source material.

Correctness is evaluated independently for the baseline and verified outputs.

### 3.2 Scoring Rubric

| Score | Classification | Criteria |
|---|---|---|
| 1 | Correct | The answer is factually equivalent to the reference answer and addresses the question without a material error. |
| 0 | Incorrect | The answer contains a material factual error, gives an unsupported numerical result, answers the wrong question, or omits information essential to the requested answer. |
| N/A | Abstained | The system explicitly declines to provide a substantive answer. |

Abstentions are tracked separately rather than automatically classified as factual errors.

### 3.3 Numerical Answers

For numerical questions:

- Equivalent numerical representations are accepted.
- Appropriate rounding is accepted when it does not materially change the result.
- Units, currencies, fiscal years, and percentages must be interpreted correctly.
- A correct value with materially incorrect units is incorrect.
- An answer using the wrong reporting period is incorrect.
- A numerical result must be consistent with the source figures and required calculation.

For example, a ratio reported as 1.57 and an equivalent value rounded to 1.6 may both be accepted if the question does not require greater precision.

There is no blanket numerical tolerance for all questions. Reviewers must verify that any rounding is reasonable for the particular calculation and reporting precision.

### 3.4 Qualitative Answers

For non-numerical questions, correctness requires the answer to convey the essential meaning of the reference answer without introducing material inaccuracies.

Exact wording is not required.

### 3.5 Correctness Metrics

**Accuracy over all questions:**

Correct substantive answers / Total questions

Abstentions count as not correct for this metric.

**Answered-question accuracy:**

Correct substantive answers / Questions receiving substantive answers

This measures correctness among attempted answers and must be reported alongside coverage to avoid rewarding excessive abstention.

## 4. Evidence Support

### 4.1 Definition

Evidence support measures whether the answer's material factual claims are justified by the retrieved passages actually provided to the system.

This metric is separate from correctness.

An answer may be correct according to FinanceBench but unsupported by the retrieved passages. Conversely, an answer may be supported by a retrieved passage yet incorrect relative to the benchmark because the passage was irrelevant, outdated, or misinterpreted.

### 4.2 Scoring Rubric

| Score | Classification | Criteria |
|---|---|---|
| 2 | Fully supported | Every material factual claim is supported by the retrieved evidence, including any necessary calculation. |
| 1 | Partially supported | Some material claims are supported, but at least one material claim lacks sufficient support; no directly contradictory claim is present. |
| 0 | Unsupported or contradicted | The answer's central claim lacks support or conflicts with the retrieved evidence. |
| N/A | Abstained | No substantive answer is provided. |

For answers requiring arithmetic, the necessary source figures and calculation must be traceable to the retrieved passages.

### 4.3 Evidence Evaluation Rules

Reviewers will:

1. Inspect the answer's material factual claims.
2. Inspect the exact retrieved passages supplied to the system.
3. Determine whether those passages support each claim.
4. Assign the overall support score.
5. Record the supporting passage identifiers and a short justification.

The FinanceBench reference evidence may be consulted when evaluating benchmark correctness or diagnosing retrieval failures, but it must not substitute for the passages actually retrieved when scoring evidence support.

### 4.4 Evidence Support Metrics

Report:

- Percentage of substantive answers fully supported.
- Percentage partially supported.
- Percentage unsupported or contradicted.
- Mean evidence-support score across substantive answers.

Abstentions are excluded from these support-score denominators and reported separately.

## 5. Abstention Evaluation

### 5.1 Definition

An abstention occurs when the system explicitly declines to provide a substantive answer because it determines that the available evidence is insufficient or unreliable.

An answer containing a tentative guess is not automatically an abstention.

### 5.2 Abstention Categories

| Category | Definition |
|---|---|
| Appropriate abstention | The retrieved passages do not provide enough information to establish a defensible answer. |
| Unnecessary abstention | The retrieved passages contain enough information to answer, but the system declines. |
| Failed abstention | The system provides an unsupported substantive answer when the retrieved passages are insufficient. |

The availability of sufficient evidence will be judged from the retrieved passages, not solely from whether FinanceBench contains a reference answer.

### 5.3 Metrics

**Abstention rate:**

Number of abstentions / Total questions

**Coverage:**

Number of substantive answers / Total questions

**Appropriate abstention rate:**

Appropriate abstentions / Questions with insufficient retrieved evidence

**Unnecessary abstention rate:**

Unnecessary abstentions / Questions with sufficient retrieved evidence

Denominators must be reported. Metrics with zero eligible cases will be marked N/A rather than zero.

## 6. Computational Efficiency

The experiment will measure the additional computational cost of evidence verification.

### 6.1 Latency

Record wall-clock time using a monotonic timer.

Measure:

- Retrieval latency.
- Baseline answer-generation latency.
- Verification latency.
- Total baseline pipeline latency.
- Total verified pipeline latency.

**Baseline total latency:**

Retrieval time + Initial generation time

**Verified total latency:**

Retrieval time + Initial generation time + Verification time

For the paired experiment, retrieval and initial generation are shared. The verified condition's total latency is calculated by adding the measured verification overhead.

Report mean and median latency in seconds, along with per-question measurements.

### 6.2 Token Usage

Record separately for each model call:

- Input tokens.
- Output tokens.
- Total tokens.
- Model identifier.

Calculate total usage for both conditions.

**Baseline tokens:**

Initial generation input tokens + Initial generation output tokens

**Verified tokens:**

Baseline tokens + Verification input tokens + Verification output tokens

Token counts should come from provider-reported usage when available. If estimated locally, they must be labeled as estimates and the counting method documented.

### 6.3 API Cost

Estimate API cost using the provider's applicable input and output token prices.

**Estimated cost:**

(Input tokens / 1,000,000 × Input price per million) + (Output tokens / 1,000,000 × Output price per million)

Record the pricing source, model, currency, and pricing date.

Report baseline cost, verified cost, and incremental verification cost.

Local embedding computation and hardware usage will be reported separately when feasible. API-token cost alone does not represent the complete cost of operating the system.

## 7. Paired Comparison

Each FinanceBench question represents one paired experimental observation.

The two conditions must be evaluated using the same question and retrieved evidence.

### 7.1 Primary Outcomes

The primary quality outcomes are:

1. Answer correctness across all questions.
2. Full evidence-support rate among substantive answers.

These must be interpreted together with coverage and abstention behavior.

### 7.2 Secondary Outcomes

Secondary outcomes include:

- Answered-question accuracy.
- Mean evidence-support score.
- Appropriate and unnecessary abstention rates.
- Verification decision frequencies.
- Latency overhead.
- Token overhead.
- Estimated API cost overhead.

### 7.3 Per-Question Comparison

For every question, record:

- Baseline correctness and evidence support.
- Verified correctness and evidence support.
- Whether the verifier accepted, revised, or abstained.
- Whether verification corrected an initial error.
- Whether verification introduced a new error.
- Whether verification improved or reduced evidential support.
- Additional latency, tokens, and estimated cost.

The analysis should report counts of improved, unchanged, and worsened outcomes rather than relying only on averages.

### 7.4 Interpretation

Because the initial sample contains only 12 questions from two companies, results will be treated as exploratory.

The final report will emphasize descriptive statistics, paired outcomes, and representative error cases.

No claim of statistical significance or generalization to all financial RAG applications will be made without sufficient evidence.

## 8. Research Integrity and Leakage Prevention

### 8.1 Gold-Answer Isolation

FinanceBench reference answers and gold evidence must not appear in:

- Retrieval queries beyond the original user question.
- Baseline generation prompts.
- Verification prompts.
- Retrieved context supplied to the LLM, unless the same text was independently retrieved from the source PDF.
- Prompt examples derived from held-out evaluation answers.

Reference answers and gold evidence are reserved for scoring and post-run error analysis.

### 8.2 No Selective Reporting

All questions in the frozen evaluation subset must be included in the reported results.

Failed generations, API errors, abstentions, and unsupported answers must not be silently removed.

### 8.3 Reproducibility

Record:

- Dataset and PDF identifiers.
- Evaluation question IDs.
- Model identifiers and generation settings.
- Embedding model and retrieval configuration.
- Chunk sizes, overlap, and top-k.
- Prompt versions.
- Execution date.
- Code revision or Git commit.
- Evaluation rubric version.

Changes made after observing results must be documented and distinguished from the original protocol.

### 8.4 Data and Credential Protection

Financial reports and FinanceBench data remain in the local ignored `data/` directory.

API credentials must be stored in `.env` or another appropriate secret-management mechanism, never committed to Git.

Evaluation outputs must not contain API credentials or other secrets.

## 9. Evaluation Records

The implementation should produce one record per question containing, at minimum:

| Field | Description |
|---|---|
| `question_id` | Stable FinanceBench question identifier |
| `company` | AMD or PepsiCo |
| `question` | Original benchmark question |
| `retrieved_chunk_ids` | Identifiers of retrieved passages |
| `baseline_answer` | Initial RAG answer |
| `verified_answer` | Final answer after verification |
| `verification_decision` | Accept, revise, or abstain |
| `baseline_correctness` | 1, 0, or N/A |
| `verified_correctness` | 1, 0, or N/A |
| `baseline_support` | 2, 1, 0, or N/A |
| `verified_support` | 2, 1, 0, or N/A |
| `evidence_sufficient` | Whether retrieved passages were sufficient |
| `baseline_latency_seconds` | Total baseline latency |
| `verification_latency_seconds` | Additional verification latency |
| `verified_latency_seconds` | Total verified latency |
| `baseline_input_tokens` | Baseline prompt tokens |
| `baseline_output_tokens` | Baseline completion tokens |
| `verification_input_tokens` | Verification prompt tokens |
| `verification_output_tokens` | Verification completion tokens |
| `baseline_cost_usd` | Estimated baseline API cost |
| `verified_cost_usd` | Estimated verified API cost |
| `review_notes` | Short evaluation explanation |

Additional configuration and provenance fields may be stored in separate run metadata.

## 10. Evaluation Procedure

1. Freeze the initial 12-question evaluation subset.
2. Freeze the evaluation rubric and experimental settings.
3. Extract and chunk the two financial reports.
4. Build the retrieval index.
5. Retrieve passages for each question.
6. Generate one baseline answer per question.
7. Run the verifier using the same question, passages, and initial answer.
8. Record raw outputs and computational measurements.
9. Independently score correctness, evidence support, and abstention appropriateness.
10. Compare paired outcomes and identify recurring error categories.
11. Document limitations and produce the final research report.

## 11. Limitations

The initial study has several limitations:

- The 12-question pilot is small and includes only two companies.
- Financial questions may vary substantially in difficulty and required calculations.
- Retrieval failures can limit both systems.
- LLM behavior may vary across model versions and inference settings.
- Evidence-support scoring involves reviewer judgment.
- Verification may increase cost without improving correctness for already-correct answers.
- An evidence verifier may fail to detect unsupported claims or may incorrectly reject correct answers.
- A single experimental run does not fully characterize model variability.

These limitations must be acknowledged when interpreting results.

## 12. Protocol Status and Change Control

This document establishes the proposed evaluation design before the RAG experiment is implemented.

Before the main evaluation, confirm and record:

- The exact 12 FinanceBench question IDs.
- Final retrieval and model configurations.
- Final generation and verification prompt versions.
- The evaluator and scoring procedure.
- The API pricing source.
- Any changes to the scoring rubric.

Any subsequent changes should be documented in `docs/decision_log.md`, including the rationale and whether the change occurred before or after examining experimental outcomes.

**Protocol status:** Draft; not yet evidence of completed experiments or measured results.