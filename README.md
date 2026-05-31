<div align="center">

# SNUBH AI Cookbook

**Validated prompts, workflows, and evaluation protocols for clinical AI translation — built by practicing clinicians.**

`{ vibe.lab }` · SNUBH · Established Clinicians

[![License: MIT](https://img.shields.io/badge/License-MIT-1FB85C.svg)](LICENSE)

</div>

---

## What this is

An openly licensed collection of **recipes** — each one a self-contained, validated way to apply a large language model (primarily [Claude](https://claude.ai)) to a concrete clinical or research task at a tertiary academic medical center.

This is **not** a dump of production applications. Working tools live in their own repositories. This cookbook captures the *generalizable, validated method* extracted from that work: the prompt, the workflow, how it was checked, and where it breaks.

A recipe is the unit. Each teaches **one pattern** for **one clinical problem**, and is written so a colleague in another specialty can read it, run it, and adapt it.

> **Why a cookbook from clinicians?** The next bottleneck in clinical AI is not model development but translation — turning validated models into the mundane workflows physicians actually run. The people best placed to write those recipes are the clinician-investigators who already understand both the AI and the workflow. This repository is that knowledge, made portable. It is also deliberately built for **non-English-language clinical environments** — an underserved area in clinical AI reproducibility.

## How it's organized

```
cookbook/
├── README.md            ← you are here
├── CONTRIBUTING.md      ← 기여 방법 (한국어)
├── LICENSE              ← MIT
├── registry.yml         ← single source of truth: index of every recipe
└── recipes/
    ├── _TEMPLATE/       ← copy this folder to start a new recipe
    ├── radiology/
    ├── cardiology/
    ├── surgery/
    ├── pathology/
    ├── gyn-onc/
    ├── ent/
    ├── dentistry/
    ├── psychiatry/
    ├── oncology/
    └── shared/          ← cross-specialty patterns (korean-clinical-text,
                           report-drafting, cohort-extraction, eval-protocols …)
```

Two axes find every recipe: **by specialty** (the folder) and **by pattern** (the `patterns:` tag in `registry.yml`). The `shared/` folder holds recipes that aren't owned by one specialty — Korean clinical-text handling being the obvious first one.

## Index

> Generated from `registry.yml`. (A small script can keep this table in sync — see CONTRIBUTING.)

| Recipe | Specialty | Patterns | Tool | Status |
|---|---|---|---|---|
| [PI-RADS 보고서 준수 자동 점검](recipes/radiology/pirads-adherence-check/) | Radiology | report-qa, korean-clinical-text | API | draft |

`status`: `draft` → `tested` → `validated` → `in-production`

## Using a recipe

1. Open the recipe's `recipe.md`.
2. Check **준비물 (Setup)** — which tool (Claude app / Claude Code / API), what you need.
3. Copy the prompt or follow the workflow.
4. **Read 주의사항 (Caveats) first.** Every recipe states what it does *not* do and where clinical judgment is still required.

## Ground rules (non-negotiable)

- **No patient data, ever.** No identifiable patient information in any commit, prompt, or API call. Inputs are synthetic, de-identified (HIPAA Safe Harbor / PIPA), or from openly licensed sources.
- **Secret scanning + push protection** are enabled organization-wide. No API keys in commits — use environment variables.
- **A recipe is not a clinical decision.** Every recipe names the human-review points. LLM output is assistive, not authoritative.

## Contributing

See **[CONTRIBUTING.md](CONTRIBUTING.md)**. New here? Start by copying `recipes/_TEMPLATE/`. *"모르는 것은 자랑입니다."*

## License

[MIT](LICENSE) — use, modify, and share freely.

---

<div align="center">
<sub>SNUBH Vibe Lab — a multi-specialty clinician-investigator consortium at Seoul National University Bundang Hospital.</sub>
</div>
