#!/usr/bin/env python3
"""
WordPress 커스텀 CSS 주입
Pretendard 폰트 + 카드 레이아웃 + 깔끔한 네비게이션
"""
import os, sys, base64, requests, json

WP_URL = os.environ.get("WP_URL", "").rstrip("/")
WP_USER = os.environ.get("WP_USERNAME", "")
WP_PASS = os.environ.get("WP_APP_PASSWORD", "")

if not all([WP_URL, WP_USER, WP_PASS]):
    print("ERROR: WP_URL, WP_USERNAME, WP_APP_PASSWORD 환경변수 필요")
    sys.exit(1)

cred = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {cred}",
    "Content-Type": "application/json",
}

CUSTOM_CSS = """
/* AutoBlog Custom Theme — Performance-First */

@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');

* { font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important; }

body { background: #f8fafc !important; color: #1e293b; line-height: 1.7; }

/* 헤더 */
.site-header, header#masthead {
  background: #fff !important;
  border-bottom: 1px solid #e2e8f0 !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
.site-title, .site-title a {
  font-size: 22px !important; font-weight: 800 !important;
  color: #1a1a2e !important; text-decoration: none !important;
}
.site-description { font-size: 13px !important; color: #94a3b8 !important; }

/* 네비게이션 */
.main-navigation ul, .primary-navigation ul {
  display: flex !important; gap: 4px !important; list-style: none !important;
  padding: 0 !important; flex-wrap: wrap; justify-content: center;
}
.main-navigation li a, .primary-navigation li a, .wp-block-navigation-item a {
  padding: 10px 18px !important; font-size: 14px !important; font-weight: 600 !important;
  color: #475569 !important; text-decoration: none !important;
  border-radius: 8px !important; transition: all 0.2s ease !important;
}
.main-navigation li a:hover, .primary-navigation li a:hover { background: #f1f5f9 !important; color: #6366f1 !important; }
.main-navigation li.current-menu-item a { background: rgba(99,102,241,0.08) !important; color: #6366f1 !important; }

/* 콘텐츠 영역 */
.site-content, .content-area, main#main {
  max-width: 1200px !important; margin: 0 auto !important; padding: 32px 20px !important;
}

/* 카드 레이아웃 */
.site-main > article, .hentry {
  background: #fff !important; border-radius: 16px !important;
  border: 1px solid #e2e8f0 !important; padding: 28px 32px !important;
  margin-bottom: 20px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
  transition: all 0.2s ease !important;
}
.site-main > article:hover, .hentry:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
  transform: translateY(-2px);
}

/* 글 제목 */
.entry-title, .entry-title a {
  font-size: 20px !important; font-weight: 800 !important;
  color: #1a1a2e !important; text-decoration: none !important; line-height: 1.4 !important;
}
.entry-title a:hover { color: #6366f1 !important; }

/* 메타 */
.entry-meta, .entry-meta a, .posted-on, .byline { font-size: 13px !important; color: #94a3b8 !important; }
.entry-meta a { color: #6366f1 !important; text-decoration: none !important; font-weight: 600; }

/* 발췌 */
.entry-summary { font-size: 15px !important; color: #64748b !important; line-height: 1.7 !important; }

/* 카테고리 배지 */
.cat-links a {
  display: inline-block; padding: 3px 10px !important;
  background: rgba(99,102,241,0.08) !important; color: #6366f1 !important;
  border-radius: 6px !important; font-size: 11px !important; font-weight: 700 !important;
}

/* 더 읽기 */
.more-link {
  display: inline-block; padding: 8px 20px !important;
  background: #6366f1 !important; color: #fff !important;
  border-radius: 8px !important; font-size: 13px !important; font-weight: 700 !important;
  text-decoration: none !important; transition: all 0.2s ease !important;
}
.more-link:hover { background: #4f46e5 !important; }

/* 단일 글 */
.single .entry-content { max-width: 768px !important; margin: 0 auto !important; }
.single .entry-title { font-size: 28px !important; text-align: center; }
.single .entry-meta { text-align: center; margin-bottom: 32px !important; }

/* 사이드바 위젯 */
.widget {
  background: #fff !important; border-radius: 12px !important;
  border: 1px solid #e2e8f0 !important; padding: 24px !important; margin-bottom: 16px !important;
}
.widget-title {
  font-size: 14px !important; font-weight: 800 !important; color: #1a1a2e !important;
  padding-bottom: 12px !important; border-bottom: 2px solid #f1f5f9 !important;
}

/* 푸터 */
.site-footer, footer#colophon {
  background: #1a1a2e !important; color: #94a3b8 !important;
  padding: 40px 20px !important; margin-top: 60px !important; text-align: center;
}
.site-footer a { color: #818cf8 !important; text-decoration: none !important; }

/* 페이지네이션 */
.nav-links { display: flex !important; justify-content: center !important; gap: 8px !important; margin: 40px 0 !important; }
.nav-links a, .nav-links span {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 40px; height: 40px; border-radius: 8px !important;
  font-size: 14px !important; font-weight: 600 !important; text-decoration: none !important;
}
.nav-links a { background: #fff !important; color: #475569 !important; border: 1px solid #e2e8f0 !important; }
.nav-links a:hover { background: #f1f5f9 !important; color: #6366f1 !important; }
.nav-links .current { background: #6366f1 !important; color: #fff !important; border: none !important; }

/* 검색 */
.search-field {
  padding: 10px 16px !important; border: 1px solid #e2e8f0 !important;
  border-radius: 8px !important; font-size: 14px !important;
}
.search-field:focus { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important; }
.search-submit {
  padding: 10px 20px !important; background: #6366f1 !important; color: #fff !important;
  border: none !important; border-radius: 8px !important; font-weight: 700 !important;
}

/* 반응형 */
@media (max-width: 768px) {
  .site-content { padding: 16px 12px !important; }
  .site-main > article, .hentry { padding: 20px !important; border-radius: 12px !important; }
  .entry-title, .entry-title a { font-size: 17px !important; }
  .single .entry-title { font-size: 22px !important; }
  .main-navigation li a { padding: 8px 12px !important; font-size: 13px !important; }
}
""".strip()


def inject_css():
    """WordPress에 커스텀 CSS 주입"""
    api = f"{WP_URL}/wp-json/wp/v2"

    # 1. 현재 테마 확인
    resp = requests.get(f"{api}/themes", headers=HEADERS, timeout=10)
    active_theme = ""
    if resp.status_code == 200:
        for t in resp.json():
            if t.get("status") == "active":
                active_theme = t.get("stylesheet", "")
                print(f"활성 테마: {active_theme}")
                break

    # 2. 기존 custom_css 포스트 찾기
    resp = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        params={"per_page": 1, "status": "publish,draft",
                "search": "custom_css", "_fields": "id"},
        headers=HEADERS, timeout=10
    )

    # 3. Customizer Additional CSS 주입 (가장 확실한 방법)
    # WP CLI 없이 REST API로: custom_css post type 직접 접근
    css_id = None

    # custom_css post type 검색 (테마 이름으로)
    if active_theme:
        resp = requests.get(
            f"{WP_URL}/wp-json/wp/v2/search",
            params={"search": active_theme, "per_page": 20},
            headers=HEADERS, timeout=10
        )
        if resp.status_code == 200:
            for item in resp.json():
                if item.get("subtype") == "custom_css":
                    css_id = item["id"]
                    print(f"기존 custom_css 포스트: id={css_id}")
                    break

    # 4. 업데이트 또는 생성
    if css_id:
        resp = requests.post(
            f"{api}/posts/{css_id}",
            headers=HEADERS,
            json={"content": CUSTOM_CSS},
            timeout=15
        )
        if resp.status_code in (200, 201):
            print(f"[OK] CSS 업데이트 완료 (id={css_id})")
            return True

    # 5. REST API로 안 되면 → CSS 파일 출력 + 수동 안내
    print("[INFO] REST API로 custom_css 직접 주입 불가")
    print("[INFO] WP Admin > 외모 > 추가 CSS에 아래 내용을 붙여넣으세요")
    print(f"\nCSS 크기: {len(CUSTOM_CSS)} bytes ({len(CUSTOM_CSS.splitlines())} lines)")

    # CSS 파일로도 저장
    css_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_theme.css")
    with open(css_file, "w", encoding="utf-8") as f:
        f.write(CUSTOM_CSS)
    print(f"CSS 파일 저장: {css_file}")

    return False


if __name__ == "__main__":
    inject_css()
