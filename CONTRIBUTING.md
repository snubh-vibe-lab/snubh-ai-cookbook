# 기여 가이드 (Contributing)

> 코드 한 줄 못 짜도 괜찮습니다. cookbook에 필요한 건 **"임상적으로 검증된 방법"**이지, 화려한 코드가 아닙니다. 막히면 테크 헬퍼에게 물어보세요. *모르는 것은 자랑입니다.*

## 한 눈에 보는 흐름

```
_TEMPLATE 폴더 복사  →  recipe.md 채우기  →  registry.yml 에 한 줄 추가  →  PR
```

## 1. 레시피 폴더 만들기

`recipes/_TEMPLATE/` 폴더를 통째로 복사해서 본인 과 아래로 옮기고 이름을 바꿉니다.

```
recipes/<specialty>/<짧은-슬러그>/
```

- `<specialty>`: `radiology` `cardiology` `surgery` `pathology` `gyn-onc` `ent` `dentistry` `psychiatry` `oncology`, 혹은 과를 안 타는 공통 패턴이면 `shared`
- `<짧은-슬러그>`: 소문자 + 하이픈. 예) `operative-note-extraction`

> GitHub 웹에서 파일을 직접 만들어도 됩니다 (터미널 몰라도 됨). "Add file" → "Create new file" → 경로에 `recipes/cardiology/내슬러그/recipe.md` 라고 치면 폴더가 자동 생성됩니다.

## 2. `recipe.md` 채우기

템플릿의 각 섹션을 채웁니다. 어렵게 생각하지 말고 **동료에게 설명하듯** 쓰면 됩니다.

| 섹션 | 핵심 |
|---|---|
| frontmatter (맨 위 `---` 블록) | `registry.yml` 항목과 똑같이. id·title·specialty·status 등 |
| 문제 | 어떤 반복 작업/병목인가 |
| 레시피 | **검증된 프롬프트를 복붙 가능하게** |
| 예시 입출력 | 합성/비식별 샘플만 |
| 검증 | 어떻게 확인했고, 안 되는 케이스는 무엇인가 (솔직하게) |
| 주의사항 | 환자정보 금지, 사람 검토가 필요한 지점 |

**`status` 정직하게:**
`draft`(아직 다듬는 중) → `tested`(내가 돌려봤다) → `validated`(데이터로 검증) → `in-production`(실제 진료/연구에 쓰는 중). draft도 환영합니다. 완벽할 필요 없습니다.

## 3. `registry.yml` 에 등록

루트의 `registry.yml` 맨 아래 `recipes:` 목록에 항목 하나를 추가합니다. (recipe.md frontmatter를 그대로 복사 + `path`, `summary` 추가)

이 한 줄이 없으면 README 인덱스에 안 뜹니다.

## 4. PR 올리기

브랜치 만들어 PR. 제목은 `[과] 레시피 제목` 형식이면 충분합니다. 동료 1명 리뷰 후 머지.

---

## 절대 하지 말 것 ⚠️

- **환자정보(이름·등록번호·생년월일 등)를 어디에도 넣지 않기** — 커밋·프롬프트·예시·API 호출 전부. 합성/비식별/공개 데이터만.
- **API 키를 커밋하지 않기** — 환경변수(`os.environ.get("ANTHROPIC_API_KEY")`)로만. org 전체에 secret scanning + push protection이 켜져 있습니다.
- 레시피를 임상 판단의 대체물처럼 쓰지 않기 — 항상 "사람 검토 지점"을 명시.

## 좋은 레시피의 특징

- 다른 과 사람이 읽고 **그대로 따라 할 수 있다**
- 프롬프트가 **복붙 가능**하다
- **안 되는 케이스**까지 솔직하게 적었다
- 한국어 임상 환경 특유의 트릭이 담겨 있다 (← 이게 우리 cookbook의 차별점)

## 막힐 때

- 테크 헬퍼에게 묻기 (모임/채널에서)
- `recipes/radiology/pirads-adherence-check/` 를 예시로 참고
- 이 cookbook 자체를 만드는 작업도 Claude에게 시키면 됩니다

---

*SNUBH Vibe Lab · "동료로서, 만든 것으로, 솔직하게."*
