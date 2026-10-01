# Evaluation Methodology

Verity v1.0 uses deterministic, auditable evaluators. Exact match is appropriate for canonical
answers; containment checks required evidence in longer text; token F1 measures lexical overlap;
JSON evaluators validate structured output; tool-call correctness compares ordered names and arguments.

The gate requires every case to satisfy its declared threshold. A baseline may additionally enforce a
maximum p95 latency regression. This makes CI failures reproducible rather than dependent on an
unstated subjective judgment.

Future extension points include Recall@K/MRR for retrieval, groundedness evaluators, pinned judge-model
runs, token/cost budgets, safety suites, and dataset versioning.
