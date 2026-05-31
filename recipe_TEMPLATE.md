---
# ── registry.yml 과 동일한 필드. 새 레시피는 이 블록부터 채우세요. ──
id: specialty-short-slug              # 예: radiology-pirads-adherence-check (소문자, 하이픈)
title: 한 줄 제목                       # 예: PI-RADS 보고서 준수 자동 점검
specialty: radiology                  # radiology | cardiology | surgery | pathology |
                                      # gyn-onc | ent | dentistry | psychiatry | oncology | shared
patterns: [report-qa, korean-clinical-text]   # 아래 "공통 패턴 태그" 중 1~3개
author: Your Name
tool: [claude-api]                    # claude-app | claude-code | claude-api | mcp (복수 가능)
model: claude-opus-4-8                # 사용·검증한 모델
status: draft                         # draft | tested | validated | in-production
data: synthetic                       # synthetic | deidentified | public  (※ raw PHI 절대 금지)
created: 2026-05-31
updated: 2026-05-31
---

# {title}

> **한 줄 요약.** 이 레시피가 어떤 임상 상황의 무엇을 자동화하는지 한 문장으로.

## 문제 — 왜 만들었나

진료·연구 현장의 어떤 반복 작업, 어떤 병목인지. "이것만 자동화되면 좋겠는데"를 구체적으로.
(예: 전립선 MRI 판독문이 PI-RADS 구조를 빠짐없이 따랐는지 사람이 일일이 확인하는 데 시간이 든다.)

## 무엇을 하나

입력 → 처리 → 출력을 2~3줄로. 무엇을 *하지 않는지*도 명시 (범위 한정).

## 준비물

- **도구:** Claude (app / Code / API 중 무엇)
- **계정·키:** (API면 키 필요 / app이면 불필요 등)
- **의존성:** Python 패키지, MCP 커넥터 등 (있으면)
- **입력 형식:** (예: 텍스트 판독문 1건, .csv 코호트 등)

## 레시피

검증된 프롬프트·워크플로우를 **복붙 가능한 형태로**. 프롬프트가 길면 `prompt.md`로 분리하고 여기선 링크.

```text
[검증된 프롬프트 본문 — 여기에 그대로]
```

여러 단계면 번호로:

1. …
2. …

## 예시 입력 · 출력

**입력 (합성/비식별 데이터만):**

```text
[샘플 입력 — assets/sample_input.txt 로 빼도 됨]
```

**출력:**

```text
[Claude 응답 예시]
```

## 검증

- **어떻게 검증했나:** (예: 과거 판독문 73건에 적용, 2명 판독의 기준과 대조)
- **결과:** (정확도/일치율/실패 사례 — 솔직하게. 안 되는 케이스도 적기)
- **status 근거:** 왜 draft/tested/validated 인지

## 주의사항 · 안전

- **데이터:** 이 레시피에 raw 환자정보를 넣지 말 것. 비식별/합성/공개 데이터만.
- **할루시네이션 위험:** 임상 판단을 대체하지 않음. 사람 검토가 필요한 지점 명시.
- **한계:** 적용 안 되는 환자군·상황.

## 다른 과로 재사용하기

이 패턴을 다른 specialty에서 쓰려면 무엇만 바꾸면 되는지. (cookbook의 진짜 가치 — cross-specialty 전파)

---

*SNUBH Vibe Lab · MIT License · 본 레시피의 코드/프롬프트는 자유롭게 사용·수정 가능*
