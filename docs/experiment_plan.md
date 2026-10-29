
# Experiment Plan — Evaluating Evidence Verification in Financial RAG

**Course:** Cloud Computing — Fall 2026  
**Project Type:** Individual Peer Reviewed Project (PRWd)  
**Status:** Planning / Preliminary Validation  
**Version:** 0.1 — Initial Draft  
**Created:** October 29, 2026  
**Target Completion:** Fall 2026 Final Exam Period

---

## 1. Experiment Overview

This project investigates whether adding an evidence-verification step to a Retrieval-Augmented Generation (RAG) system improves the reliability of answers generated from financial documents.

The experiment will compare two configurations:

1. **Baseline RAG:** Retrieves relevant financial information and generates an answer.
2. **Evidence-Verified RAG:** Uses the same retrieved information and initial answer, followed by an additional verification step that checks whether the answer is supported by the retrieved evidence.

The experiment will evaluate answer correctness, evidence support, abstention behavior, response latency, and token usage.

A secondary objective is to investigate the tradeoff between AI reliability and the computational overhead of cloud-hosted LLM inference.

## 2. Research Question and Hypotheses

### Primary Research Question

Does adding an evidence-verification step improve the reliability of financial RAG answers, and is the improvement worth the additional computational cost?

### Hypotheses

**H1 — Evidence Support**

Evidence-verified RAG will produce fewer unsupported answers than baseline RAG.

**H2 — Answer Correctness**

Evidence verification may improve answer correctness by identifying and correcting unsupported responses.

**H3 — Computational Overhead**

Evidence verification will increase inference time and token usage because it requires additional LLM calls.

**H4 — Verification Limitations**

Verification may introduce errors, reject correct answers, or abstain unnecessarily.

These hypotheses will be evaluated rather than assumed to be true.

## 3. Dataset and Experimental Sample

### Benchmark

The experiment will use FinanceBench, a financial question-answering benchmark containing questions, reference answers, and supporting evidence from financial reports.

### Initial Documents

| Document | Questions |
|---|---:|
| AMD 2022 Form 10-K | 7 |
| PepsiCo 2022 Form 10-K | 5 |
| **Total** | **12** |

The initial experiment will use all 12 identified questions.

Expansion to approximately 20 questions is optional and will depend on implementation progress.

### Dataset Preparation

- Extract financial report text using Python.
- Preserve source document and page metadata.
- Split extracted text into passages suitable for retrieval.
- Generate embeddings and build a searchable index.
- Associate each benchmark question with its corresponding financial report.

FinanceBench reference answers and annotated gold evidence will be reserved for evaluation and excluded from generation and verification prompts.

## 4. Experimental Design

The experiment will use a paired comparison in which each question is evaluated under two conditions.

### Condition A — Baseline RAG

1. Receive a FinanceBench question.
2. Retrieve relevant passages from the associated financial report.
3. Provide the question and retrieved passages to a hosted LLM.
4. Generate an answer using the retrieved evidence.
5. Record the answer, retrieved passages, latency, and token usage.

### Condition B — Evidence-Verified RAG

1. Use the same question and retrieved passages.
2. Start with the baseline system's initial generated answer.
3. Submit the answer and evidence to an additional LLM verification step.
4. Determine whether the answer is adequately supported.
5. Accept the answer, revise it once, or abstain if sufficient support is unavailable.
6. Record the verification decision, final answer, latency, and token usage.

The verified condition will include the original generation cost plus any additional verification and revision costs.

### Controlled Variables

Both conditions will use:

- The same benchmark questions.
- The same source documents.
- The same document extraction and chunking approach.
- The same embedding model and retrieval configuration.
- The same retrieved passages for each question.
- The same initial generated answer.
- Consistent generation settings.

The primary experimental difference will be the additional evidence-verification step.

## 5. Proposed Technical Stack

| Component | Proposed Technology |
|---|---|
| Programming language | Python |
| PDF extraction | PyMuPDF |
| Text embeddings | Sentence Transformers |
| Vector similarity search | FAISS |
| LLM inference | Cloud-hosted LLM API — TBD |
| Data analysis | pandas |
| Development environment | VS Code |
| Version control | Git and GitHub |

The LLM provider, model, embedding model, chunk size, overlap, and retrieval top-k will be finalized during implementation.

A complex agent framework is not required for the initial experiment.

## 6. Implementation Roadmap

### Phase 1 — Repository Setup and Dataset Validation

**Status:** In Progress

Tasks:

- [x] Select the research topic.
- [x] Select FinanceBench as the evaluation benchmark.
- [x] Obtain AMD and PepsiCo financial reports.
- [x] Verify PDF text extraction.
- [x] Identify 12 available benchmark questions.
- [x] Validate at least one financial calculation.
- [x] Initialize the GitHub repository structure.
- [x] Draft the project scope.
- [ ] Review the complete PRWd assignment requirements.
- [ ] Confirm dataset and PDF redistribution permissions.
- [ ] Finalize the initial experiment documentation.

**Completion Criteria:** The dataset, repository, and experimental scope are ready for implementation.

### Phase 2 — Document Processing and Retrieval

**Status:** Not Started

Tasks:

- [ ] Implement reusable PDF text extraction.
- [ ] Preserve document and page metadata.
- [ ] Split extracted text into retrieval chunks.
- [ ] Select an embedding model.
- [ ] Generate document embeddings.
- [ ] Build a FAISS vector index.
- [ ] Implement document-specific retrieval.
- [ ] Test retrieval on sample FinanceBench questions.
- [ ] Inspect retrieved passages for relevance.

**Completion Criteria:** Given a benchmark question, the system can retrieve relevant passages from the correct financial report.

### Phase 3 — Baseline RAG Implementation

**Status:** Not Started

Tasks:

- [ ] Select a cloud-hosted LLM provider and model.
- [ ] Configure API credentials securely.
- [ ] Develop the baseline generation prompt.
- [ ] Connect retrieval to LLM inference.
- [ ] Generate answers with source references.
- [ ] Record generated answers and retrieved passages.
- [ ] Measure response latency.
- [ ] Record input and output token usage.
- [ ] Test the baseline on a small pilot subset.

**Completion Criteria:** The baseline system generates and records answers grounded in retrieved financial passages.

### Phase 4 — Evidence Verification

**Status:** Not Started

Tasks:

- [ ] Define the verification prompt and structured response format.
- [ ] Submit baseline answers and retrieved passages for verification.
- [ ] Check whether answer claims are supported by the evidence.
- [ ] Implement accept, revise-once, or abstain behavior.
- [ ] Preserve the original baseline answer for comparison.
- [ ] Record verification decisions and final answers.
- [ ] Measure additional verification latency and token usage.
- [ ] Test verification on correct and unsupported answers.

**Completion Criteria:** The verification stage can assess baseline answers without accessing benchmark reference answers.

### Phase 5 — Evaluation and Analysis

**Status:** Not Started

Tasks:

- [ ] Finalize the evaluation protocol before the full experiment.
- [ ] Run both configurations on the same 12 questions.
- [ ] Evaluate answer correctness against FinanceBench references.
- [ ] Independently assess evidence support.
- [ ] Record accepted, revised, and abstained answers.
- [ ] Compare end-to-end latency.
- [ ] Compare total token usage.
- [ ] Estimate API costs where possible.
- [ ] Analyze retrieval, generation, and verification errors.
- [ ] Summarize findings and limitations.

**Completion Criteria:** A reproducible comparison exists between baseline and evidence-verified RAG.

### Phase 6 — Final Research Deliverables

**Status:** Not Started

Tasks:

- [ ] Organize and clean the repository.
- [ ] Update the README with setup and execution instructions.
- [ ] Prepare comparison tables or visualizations.
- [ ] Write the final PRWd paper according to course requirements.
- [ ] Include relevant research citations.
- [ ] Discuss limitations and possible improvements.
- [ ] Verify that required deliverables are complete.
- [ ] Submit the final project.

**Completion Criteria:** The experiment, analysis, and final paper meet the course requirements.

## 7. Proposed Timeline

The experiment will be completed through four approximate work periods. These are planning estimates and may be adjusted based on the final deadline.

| Work Period | Estimated Effort | Main Milestone |
|---|---|---|
| 1 — Preparation | 4–5 hours | Dataset validation and project setup |
| 2 — Baseline RAG | 5–7 hours | Working retrieval and generation pipeline |
| 3 — Verification | 4–6 hours | Working evidence-verification extension |
| 4 — Evaluation | 4–6 hours | Comparison results and final paper |

If implementation requires additional time, optional features will be reduced before core evaluation activities.

## 8. Evaluation Strategy

The experiment will compare results question by question.

### Primary Metrics

**Answer Correctness**

Whether each generated answer correctly addresses the benchmark question.

**Evidence Support**

Whether the answer's factual claims are supported by the retrieved financial passages.

### Secondary Metrics

**Abstention Rate**

The proportion of questions for which the system declines to provide a definitive answer.

**Verification Outcomes**

The number of answers accepted, revised, or rejected through abstention.

**Response Latency**

The elapsed time required to produce a final answer.

**Token Usage**

The total input and output tokens used for each condition.

**Estimated Inference Cost**

Approximate API cost based on token usage and applicable model pricing.

### Evaluation Integrity

- Benchmark reference answers will not be supplied during generation or verification.
- Both conditions will be evaluated using the same scoring criteria.
- The verification system's own judgment will not serve as the sole measure of evidence support.
- Numerical answers will be checked against benchmark values and calculations where applicable.
- Results will be interpreted as exploratory due to the small sample size.

Detailed scoring rules will be documented in `docs/evaluation_protocol.md` before the full experimental run.

## 9. Cloud Computing Relevance

The experiment relates to several concepts covered in Cloud Computing.

### Data Processing

Financial reports will be processed through extraction, chunking, embedding generation, and retrieval.

These stages relate conceptually to data-processing workflows studied through Hadoop, MapReduce, and PySpark.

Although the initial dataset does not require distributed computing, the preprocessing and indexing stages could potentially be scaled for larger document collections.

### Cloud-Based LLM Inference

The project will use a hosted LLM service to generate and verify answers.

This demonstrates how applications can access remote computational resources through cloud-based APIs.

### Computational Efficiency

The experiment will examine the relationship between answer reliability and additional inference overhead.

Measurements of latency, token usage, and estimated cost will help determine whether verification provides sufficient benefits to justify its additional computational requirements.

## 10. Risks and Contingency Plans

| Risk | Mitigation |
|---|---|
| PDF extraction loses table structure | Inspect extracted content and document limitations |
| Relevant evidence is not retrieved | Adjust chunking and retrieval parameters during development |
| LLM responses vary between runs | Use consistent prompts and generation settings |
| Verification introduces new errors | Preserve baseline answers and analyze changes |
| API costs exceed expectations | Limit sample size and verification attempts |
| Implementation takes longer than planned | Prioritize the 12-question minimum experiment |
| Results are inconclusive | Report limitations without overstating conclusions |
| Course requirements differ | Revise the plan after reviewing assignment instructions |

## 11. Minimum Viable Experiment

The minimum successful experiment will:

1. Process the AMD and PepsiCo financial reports.
2. Retrieve relevant passages for the 12 FinanceBench questions.
3. Generate baseline RAG answers.
4. Apply evidence verification to the baseline answers.
5. Evaluate correctness and evidence support for both conditions.
6. Compare latency, token usage, and abstention behavior.
7. Summarize the findings in the final PRWd paper.

Optional enhancements, including a larger sample or additional retrieval methods, will be considered only after the core experiment works.

## 12. Current Progress

As of October 29, 2026:

- FinanceBench data and two source PDFs have been obtained.
- PDF text extraction has been tested.
- Twelve benchmark questions have been identified.
- One AMD financial calculation has been independently reproduced.
- The repository structure has been initialized.
- The project scope has been drafted.

The retrieval pipeline, baseline RAG system, evidence-verification extension, and comparative evaluation have not yet been implemented.

## 13. Experiment Plan Maintenance

This is a working document and will be updated as development progresses.

Updates should reflect:

- Completed implementation milestones.
- Changes to the experimental design.
- Adjustments to the sample size or timeline.
- Technical limitations discovered during testing.
- Decisions documented in `docs/decision_log.md`.

Major changes should be recorded in the decision log, including their rationale and implications.

---

**Next Milestone:** Implement document processing, chunking, and semantic retrieval.
