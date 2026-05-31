#!/usr/bin/env python3
"""
SNUBH AI Cookbook — harvester (v2: 멤버 기반 발견)

봇은 repo 위치가 아니라 **org 멤버십**으로 돈다.
  1) snubh-vibe-lab org의 멤버 목록을 가져온다 (= 우리 org으로 인정된 사람들)
  2) 각 멤버의 **개인 계정 repo** 중 topic `snubh-cookbook` 이 달린 것만 본다
  3) 그 repo의 .cookbook/*.md 레시피를 수확한다

→ repo 소유권은 멤버 본인에게 그대로 남는다. org로 이전할 필요 없음.

제약:
- 비공개 개인 repo는 못 읽음(권한 없음). 레시피 repo는 public 이어야 함.
- 멤버가 아닌 사람의 repo는, topic을 달아도 절대 수확되지 않음(멤버십이 게이트).

환경변수:
  GH_TOKEN       org 멤버 읽기(read:org) + 이 repo 쓰기 권한 토큰
  GH_ORG         기본 "snubh-vibe-lab"
  SELF_REPO      이 cookbook repo 이름. 제외. 기본 "snubh-ai-cookbook"
  OPT_IN_TOPIC   대상 표식. 기본 "snubh-cookbook". 빈 값이면 멤버의 모든 repo 스캔(비권장)
  INCLUDE_ORG_REPOS  "1" 이면 org 소속 repo도 함께 스캔(혼합 운영). 기본 미설정.

의존성: PyYAML. 그 외 표준 라이브러리.
"""
from __future__ import annotations
import json, os, re, sys, shutil, urllib.request, urllib.error
from pathlib import Path
import yaml

ORG          = os.environ.get("GH_ORG", "snubh-vibe-lab")
SELF_REPO    = os.environ.get("SELF_REPO", "snubh-ai-cookbook")
TOKEN        = os.environ.get("GH_TOKEN", "")
OPT_IN_TOPIC = os.environ.get("OPT_IN_TOPIC", "snubh-cookbook")
INCLUDE_ORG  = os.environ.get("INCLUDE_ORG_REPOS") == "1"
API          = "https://api.github.com"

ROOT          = Path(__file__).resolve().parent.parent
RECIPES_DIR   = ROOT / "recipes"
REGISTRY_PATH = ROOT / "registry.yml"
README_PATH   = ROOT / "README.md"

REQUIRED_FIELDS = ["id", "title", "specialty", "author", "status"]
VALID_SPECIALTIES = {
    "radiology", "cardiology", "surgery", "pathology", "gyn-onc",
    "ent", "dentistry", "psychiatry", "oncology",
    "neurology", "neurosurgery", "ophthalmology", "anesthesiology",
    "pediatrics", "rehab", "family_med", "shared",
}

BLOCK_PATTERNS = {
    "Anthropic API key": re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}"),
    "generic secret":    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9\-_]{16,}"),
    "Korean RRN (주민번호)": re.compile(r"\b\d{6}[-\s]?[1-4]\d{6}\b"),
}
WARN_PATTERNS = {
    "MRN-like long digit run": re.compile(r"\b\d{8,}\b"),
    # 한글이 든 대괄호 = 미수정 템플릿 안내문. YAML 목록 [claude-api] 이나
    # 마크다운 링크 [text] 는 한글 조건 때문에 걸리지 않음.
    "미수정 템플릿 빈칸":        re.compile(r"\[[^\]\n]*[가-힣][^\]\n]*\]"),
}


def gh(path: str):
    results, url = [], f"{API}{path}"
    while url:
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "snubh-cookbook-harvester",
        })
        try:
            with urllib.request.urlopen(req) as r:
                data = json.load(r); link = r.headers.get("Link", "")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise
        results.extend(data if isinstance(data, list) else [data])
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        url = m.group(1) if m else None
    return results


def fetch_raw(download_url: str) -> str:
    req = urllib.request.Request(download_url, headers={
        "Authorization": f"Bearer {TOKEN}", "User-Agent": "snubh-cookbook-harvester"})
    with urllib.request.urlopen(req) as r:
        return r.read().decode("utf-8", errors="replace")


def discover_sources():
    """(owner, repo_name) 목록. 멤버십 + opt-in topic 기준."""
    sources = []
    members = [m["login"] for m in (gh(f"/orgs/{ORG}/members?per_page=100") or [])]
    print(f"org '{ORG}' 멤버 {len(members)}명")
    for user in members:
        repos = gh(f"/users/{user}/repos?per_page=100&type=owner") or []
        for repo in repos:
            topics = repo.get("topics") or []
            if OPT_IN_TOPIC and OPT_IN_TOPIC not in topics:
                continue
            if repo.get("private"):
                print(f"  ⚠ {user}/{repo['name']} 는 비공개 — 못 읽음, 건너뜀")
                continue
            sources.append((user, repo["name"]))
    if INCLUDE_ORG:
        for repo in gh(f"/orgs/{ORG}/repos?per_page=100&type=all") or []:
            if repo["name"] != SELF_REPO:
                sources.append((ORG, repo["name"]))
    return sources


def parse_frontmatter(text: str):
    if not text.lstrip().startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None, text
    return meta, parts[2].lstrip("\n")


def scan_content(text: str):
    blocks = [n for n, p in BLOCK_PATTERNS.items() if p.search(text)]
    warns  = [n for n, p in WARN_PATTERNS.items()  if p.search(text)]
    return blocks, warns


def validate(meta, raw_text, where):
    if not meta:
        return f"{where}: frontmatter 없음/파싱 실패"
    missing = [f for f in REQUIRED_FIELDS if not meta.get(f)]
    if missing:
        return f"{where}: 필수 필드 누락 {missing}"
    if meta.get("specialty") not in VALID_SPECIALTIES:
        return f"{where}: specialty '{meta.get('specialty')}' 가 목록에 없음"
    blocks, _ = scan_content(raw_text)
    if blocks:
        return f"{where}: 차단 패턴 {blocks} (PHI/secret — 채택 거부)"
    return None


def main():
    if not TOKEN:
        sys.exit("GH_TOKEN 환경변수가 필요합니다.")
    sources = discover_sources()
    print(f"수확 대상 repo {len(sources)}개\n")
    harvested, failures, warnings = [], [], []
    for owner, name in sources:
        contents = gh(f"/repos/{owner}/{name}/contents/.cookbook")
        if not contents:
            continue
        for item in contents:
            if item["type"] != "file" or not item["name"].endswith(".md"):
                continue
            where = f"{owner}/{name}/.cookbook/{item['name']}"
            text = fetch_raw(item["download_url"])
            meta, body = parse_frontmatter(text)
            err = validate(meta, text, where)
            if err:
                failures.append(err); continue
            _, warns = scan_content(text)
            warnings += [f"{where}: {w}" for w in warns]
            meta["source"] = f"https://github.com/{owner}/{name}/blob/HEAD/.cookbook/{item['name']}"
            meta["synced_from"] = f"{owner}/{name}"
            harvested.append((meta, body))
    write_recipes(harvested); write_registry(harvested); write_readme_index(harvested)
    print(f"수확 {len(harvested)}건 / 차단 {len(failures)}건 / 경고 {len(warnings)}건")
    for w in warnings: print("  ⚠", w)
    if failures:
        print("\n채택 거부:")
        for f in failures: print("  ✖", f)
        sys.exit(1)


def write_recipes(harvested):
    if RECIPES_DIR.exists():
        for c in RECIPES_DIR.iterdir():
            if c.name == "_TEMPLATE": continue
            shutil.rmtree(c) if c.is_dir() else c.unlink()
    for meta, body in harvested:
        dest = RECIPES_DIR / meta["specialty"] / meta["id"]; dest.mkdir(parents=True, exist_ok=True)
        fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip()
        (dest / "recipe.md").write_text(
            f"---\n{fm}\n---\n\n<!-- 자동 생성. 편집은 원본 repo의 .cookbook/ 에서. -->\n"
            f"<!-- 원본: {meta['source']} -->\n\n{body}", encoding="utf-8")


def write_registry(harvested):
    header = REGISTRY_PATH.read_text(encoding="utf-8").split("recipes:")[0] if REGISTRY_PATH.exists() else ""
    entries = [{
        "id": m["id"], "title": m["title"], "specialty": m["specialty"],
        "patterns": m.get("patterns", []), "author": m["author"], "tool": m.get("tool", []),
        "model": m.get("model", ""), "status": m["status"], "data": m.get("data", ""),
        "path": f"recipes/{m['specialty']}/{m['id']}/", "source": m["source"],
        "summary": m.get("summary", ""),
    } for m, _ in sorted(harvested, key=lambda x: (x[0]["specialty"], x[0]["id"]))]
    REGISTRY_PATH.write_text((header or "") + yaml.safe_dump({"recipes": entries}, allow_unicode=True, sort_keys=False), encoding="utf-8")


def write_readme_index(harvested):
    rows = ["| Recipe | Specialty | Patterns | Tool | Status |", "|---|---|---|---|---|"]
    for m, _ in sorted(harvested, key=lambda x: (x[0]["specialty"], x[0]["id"])):
        rows.append(f"| [{m['title']}](recipes/{m['specialty']}/{m['id']}/) | {m['specialty']} | "
                    f"{', '.join(m.get('patterns', []))} | {', '.join(m.get('tool', []))} | {m['status']} |")
    S, E = "<!-- COOKBOOK:INDEX:START -->", "<!-- COOKBOOK:INDEX:END -->"
    text = README_PATH.read_text(encoding="utf-8"); block = f"{S}\n" + "\n".join(rows) + f"\n{E}"
    if S in text and E in text:
        text = re.sub(re.escape(S) + r".*?" + re.escape(E), block, text, flags=re.S)
    else:
        text = re.sub(r"(##\s*Index[^\n]*\n)", r"\1\n" + block + "\n", text, count=1)
    README_PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
