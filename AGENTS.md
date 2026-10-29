
# AGENTS.md — RAG Evidence Verification

## Project Overview

This repository contains an individual Cloud Computing research project investigating whether evidence verification improves the reliability of Retrieval-Augmented Generation (RAG) on financial questions.

The experiment compares baseline RAG against evidence-verified RAG using FinanceBench.

Read the following documents before making significant changes:

- `README.md`
- `docs/project_scope.md`
- `docs/experiment_plan.md`
- `docs/decision_log.md`

## 1. Privacy and Sensitive Information

- Do not expose, print, commit, or publish API keys, access tokens, passwords, or other credentials.
- Do not include personal email addresses, phone numbers, private account information, or unrelated personal details in generated documentation, logs, or code.
- Do not copy local environment variables or `.env` contents into responses, commits, or generated files.
- Do not upload local datasets, financial PDFs, or repository contents to external services without explicit authorization.
- Treat files under `data/` as local research materials. Do not commit them unless redistribution permissions have been reviewed and explicit approval has been given.
- Do not include private filesystem paths or machine-specific usernames in public-facing documentation.
- If sensitive information is discovered, report the issue without reproducing the sensitive value.

## 2. Repository and Git Safety

- Respect `.gitignore`.
- Do not modify Git history, force-push, or delete files without explicit authorization.
- Do not automatically commit or push changes unless explicitly requested.
- Do not add unnecessary dependencies.
- Keep generated experiment outputs separate from source code.
- Prefer small, reviewable changes.

## 3. Research Integrity

- Never fabricate experimental results, evaluation scores, citations, or benchmark outcomes.
- Clearly distinguish implemented features from proposed features.
- Do not claim that a system has been tested unless tests were actually executed.
- Preserve benchmark reference answers for evaluation only.
- Do not expose gold answers or annotated gold evidence to generation or verification prompts.
- Keep baseline and verified RAG comparisons consistent.
- Report failures and limitations accurately.

## 4. Experimental Controls

The baseline and verified configurations should use:

- The same benchmark questions.
- The same source documents.
- The same retrieved passages.
- The same initial generated answers.
- Consistent model settings.

The verified configuration may add verification and at most one revision attempt, subject to the finalized experimental design.

Record latency and token usage separately for generation, verification, and revision where possible.

## 5. Coding Conventions

- Use Python for the implementation.
- Prefer simple, readable, modular code.
- Preserve source document and page metadata.
- Use reproducible configuration settings.
- Keep API credentials outside source code.
- Add tests for important processing and evaluation functions.
- Avoid unnecessary frameworks or infrastructure.
- Document dependencies in `requirements.txt`.

## 6. Documentation

- Update documentation when implementation decisions materially change.
- Record significant research and architecture decisions in `docs/decision_log.md`.
- Use the decision log format established in that file.
- Keep the newest decisions at the top.
- Preserve earlier decisions when superseded.
- Do not mark proposed features as completed.

## 7. Before Making Major Changes

Before introducing a new dependency, changing the retrieval architecture, modifying evaluation criteria, or expanding project scope:

1. Review the relevant project documentation.
2. Explain the proposed change and its rationale.
3. Identify potential effects on reproducibility and evaluation.
4. Request approval before making substantial architectural changes.

## 8. Scope Boundaries

Prioritize a small, reproducible experiment.

Do not introduce:

- Model fine-tuning.
- Complex autonomous agent frameworks.
- Production web infrastructure.
- Hadoop or Spark without a clear technical need.
- Unnecessary additional benchmarks.

The initial experiment uses 12 FinanceBench questions from AMD and PepsiCo 2022 Form 10-K reports.

## 9. Communication

- Explain significant changes clearly.
- Identify assumptions and unresolved questions.
- Do not silently modify experimental methodology.
- Prefer correctness, reproducibility, and transparency over unnecessary complexity.
