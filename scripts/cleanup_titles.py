#!/usr/bin/env python3
"""
WordPress 기존 글 제목에서 해시값 오염 일괄 제거
- 12자리 hex 해시 (예: dc3c547487a0, fa774c6a4d84)
- 괄호 안 해시 (예: (e89f30c984f2))
- "태그" 프리픽스
"""
import os, sys, re, base64

WP_URL = os.environ.get("WP_URL", "").rstrip("/")
WP_USER = os.environ.get("WP_USERNAME", "")
WP_PASS = os.environ.get("WP_APP_PASSWORD", "")
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"

if not all([WP_URL, WP_USER, WP_PASS]):
    print("ERROR: WP_URL, WP_USERNAME, WP_APP_PASSWORD 환경변수 필요")
    sys.exit(1)

import requests

cred = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {cred}",
    "Content-Type": "application/json",
    "User-Agent": "AutoBlog/1.0",
}
API = f"{WP_URL}/wp-json/wp/v2"


def sanitize_title(title):
    """제목에서 해시값 및 오염 패턴 제거"""
    original = title
    # 12자리 hex 해시 제거
    title = re.sub(r'\b[0-9a-f]{12}\b', '', title)
    # 괄호 안 해시 제거
    title = re.sub(r'\([0-9a-f]{10,}\)', '', title)
    # "태그" 프리픽스 제거
    title = re.sub(r'^태그\s*', '', title)
    # 정리: 연속 공백, 콤마, 콜론
    title = re.sub(r'\s*,\s*,', ',', title)
    title = re.sub(r':\s*-\s*', ': ', title)
    title = re.sub(r':\s*,', ':', title)
    title = re.sub(r'\s{2,}', ' ', title)
    title = title.strip().strip(':').strip(',').strip()
    return title if title != original else None


def fetch_all_posts():
    """모든 글 가져오기 (페이지네이션)"""
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{API}/posts",
            params={"per_page": 100, "page": page, "status": "publish,draft,pending"},
            headers=HEADERS, timeout=15
        )
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        posts.extend(batch)
        page += 1
        # WP returns total pages in header
        total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
        if page > total_pages:
            break
    return posts


def update_post_title(post_id, new_title):
    """글 제목 업데이트"""
    resp = requests.post(
        f"{API}/posts/{post_id}",
        headers=HEADERS,
        json={"title": new_title},
        timeout=15
    )
    return resp.status_code == 200


def main():
    mode = "DRY RUN" if DRY_RUN else "LIVE"
    print(f"=== 제목 해시 정리 [{mode}] ===")
    print(f"  사이트: {WP_URL}")
    print()

    posts = fetch_all_posts()
    print(f"총 {len(posts)}개 글 확인")
    print()

    dirty = 0
    fixed = 0
    errors = 0

    for post in posts:
        title = post["title"]["rendered"]
        cleaned = sanitize_title(title)

        if cleaned is not None:
            dirty += 1
            print(f"  [{post['id']}] DIRTY")
            print(f"    before: {title[:80]}")
            print(f"    after:  {cleaned[:80]}")

            if not DRY_RUN:
                if update_post_title(post["id"], cleaned):
                    fixed += 1
                    print(f"    -> FIXED")
                else:
                    errors += 1
                    print(f"    -> ERROR")
            else:
                print(f"    -> (dry run)")
            print()

    print(f"=== 결과 ===")
    print(f"  총 글: {len(posts)}")
    print(f"  오염 발견: {dirty}")
    if not DRY_RUN:
        print(f"  수정 완료: {fixed}")
        print(f"  수정 실패: {errors}")
    else:
        print(f"  (DRY_RUN=true — 실제 수정 없음)")


if __name__ == "__main__":
    main()
