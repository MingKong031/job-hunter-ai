#!/usr/bin/env python3
"""job-hunter-ai 发布脚本：走 GitHub Contents API（git 通道被沙箱限制）。

用法:
    python upload_repo.py <token> [--dry-run]
功能:
    1. 新增 docs/ats-adaptation-guide.md、docs/feishu-auto-apply.md（PUT, 无需 sha）
    2. 更新 README.md（先 GET 拿 sha 再 PUT 覆盖）
"""
import base64
import json
import sys
import urllib.request

REPO = "MingKong031/job-hunter-ai"
BRANCH = "main"
BASE = f"https://api.github.com/repos/{REPO}/contents"

FILES = [
    "docs/ats-adaptation-guide.md",
    "docs/feishu-auto-apply.md",
    "README.md",
    "scripts/upload_repo.py",
]

def api(url, token, method="GET", data=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data=body, timeout=30) as resp:
            raw = resp.read()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, json.loads(raw) if raw else {}

def main():
    if len(sys.argv) < 2:
        print("usage: upload_repo.py <token> [--dry-run]")
        sys.exit(1)
    token = sys.argv[1]
    dry = "--dry-run" in sys.argv

    for path in FILES:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        encoded = base64.b64encode(content.encode()).decode()

        # 已存在则先拿 sha
        sha = None
        status, existing = api(f"{BASE}/{path}?ref={BRANCH}", token)
        if status == 200 and "sha" in existing:
            sha = existing["sha"]
        elif status == 404:
            sha = None
        else:
            print(f"[{path}] 查询失败: {status} {existing.get('message','')}")
            sys.exit(1)

        payload = {
            "message": f"docs: 更新 {path}",
            "content": encoded,
            "branch": BRANCH,
        }
        if sha:
            payload["sha"] = sha

        if dry:
            print(f"[{path}] dry-run: {'更新' if sha else '新增'} (sha={sha[:8] if sha else '无'})")
            continue

        status, resp = api(f"{BASE}/{path}", token, method="PUT", data=payload)
        if status in (200, 201):
            print(f"[OK] {path} → {resp.get('commit',{}).get('sha','')[:10]}")
        else:
            print(f"[FAIL] {path}: {status} {resp.get('message','')}")
            if "sha" in str(resp.get('message','')):
                print("  → 远程已变更，需先同步")
            sys.exit(1)

    print("全部完成" if not dry else "dry-run 完成，未实际写入")

if __name__ == "__main__":
    main()
