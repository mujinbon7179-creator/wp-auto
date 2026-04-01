#!/usr/bin/env python3
"""
WordPress Customizer에 CSS 자동 주입 (브라우저 없이)
1. wp-login.php로 세션 쿠키 획득
2. customize.php에서 nonce 추출
3. admin-ajax.php로 CSS 저장
"""
import os, sys, re, json, uuid

WP_URL = os.environ.get("WP_URL", "").rstrip("/")
WP_USER = os.environ.get("WP_USERNAME", "")
WP_PASS = os.environ.get("WP_APP_PASSWORD", "")
WP_LOGIN_PASS = os.environ.get("WP_LOGIN_PASSWORD", "")

# WP_LOGIN_PASSWORD가 없으면 WP_APP_PASSWORD 시도
login_pass = WP_LOGIN_PASS or WP_PASS

if not all([WP_URL, WP_USER, login_pass]):
    print("ERROR: WP_URL, WP_USERNAME, WP_LOGIN_PASSWORD (또는 WP_APP_PASSWORD) 필요")
    sys.exit(1)

import requests

session = requests.Session()
session.headers.update({"User-Agent": "AutoBlog/1.0"})

# CSS 파일 로드
css_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_theme.css")
if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        CUSTOM_CSS = f.read()
    print(f"CSS 로드: {len(CUSTOM_CSS)} bytes from {css_file}")
else:
    print(f"ERROR: {css_file} 없음")
    sys.exit(1)

domain = WP_URL.replace("https://", "").replace("http://", "").split("/")[0]


def step1_login():
    """WordPress 로그인 → 세션 쿠키 획득"""
    print(f"\n=== Step 1: 로그인 ({domain}) ===")

    # 테스트 쿠키 설정 (WordPress 요구사항)
    session.cookies.set("wordpress_test_cookie", "WP+Cookie+check", domain=domain)

    resp = session.post(
        f"{WP_URL}/wp-login.php",
        data={
            "log": WP_USER,
            "pwd": login_pass,
            "wp-submit": "Log In",
            "redirect_to": f"{WP_URL}/wp-admin/",
            "testcookie": "1",
        },
        allow_redirects=True,
        timeout=30,
    )

    # 로그인 성공 여부 확인
    if "wp-admin" in resp.url and "wp-login" not in resp.url:
        print(f"  [OK] 로그인 성공 → {resp.url}")
        return True

    if "wp-login.php" in resp.url:
        if "incorrect" in resp.text.lower():
            print(f"  [ERR] 비밀번호 틀림")
        elif "cookie" in resp.text.lower():
            print(f"  [ERR] 쿠키 문제")
        else:
            print(f"  [ERR] 로그인 실패: {resp.url}")
        return False

    print(f"  [OK] 로그인 성공 (리다이렉트: {resp.url})")
    return True


def step2_get_nonce():
    """Customizer 페이지에서 nonce + 테마 정보 추출"""
    print(f"\n=== Step 2: Customizer nonce 추출 ===")

    resp = session.get(
        f"{WP_URL}/wp-admin/customize.php",
        timeout=30,
    )

    if resp.status_code != 200:
        print(f"  [ERR] Customizer 접근 실패: {resp.status_code}")
        return None, None

    # nonce 추출
    nonce_match = re.search(r'"nonce":"([a-f0-9]+)"', resp.text)
    if not nonce_match:
        nonce_match = re.search(r'_wpnonce=([a-f0-9]+)', resp.text)
    if not nonce_match:
        nonce_match = re.search(r'"customize-save"\s*:\s*"([a-f0-9]+)"', resp.text)

    nonce = nonce_match.group(1) if nonce_match else None

    # 활성 테마 추출
    theme_match = re.search(r'"stylesheet"\s*:\s*"([^"]+)"', resp.text)
    if not theme_match:
        theme_match = re.search(r'custom_css\[([^\]]+)\]', resp.text)

    theme = theme_match.group(1) if theme_match else None

    # changeset UUID 추출
    changeset_match = re.search(r'"changeset_uuid"\s*:\s*"([^"]+)"', resp.text)
    changeset_uuid = changeset_match.group(1) if changeset_match else str(uuid.uuid4())

    print(f"  nonce: {nonce}")
    print(f"  theme: {theme}")
    print(f"  changeset: {changeset_uuid[:8]}...")

    return nonce, theme, changeset_uuid


def step3_save_css(nonce, theme, changeset_uuid):
    """admin-ajax.php로 CSS 저장"""
    print(f"\n=== Step 3: CSS 저장 ===")

    if not nonce or not theme:
        print(f"  [ERR] nonce 또는 theme 정보 없음")
        return False

    css_key = f"custom_css[{theme}]"
    customized = json.dumps({css_key: CUSTOM_CSS})

    resp = session.post(
        f"{WP_URL}/wp-admin/admin-ajax.php",
        data={
            "action": "customize_save",
            "customize_changeset_uuid": changeset_uuid,
            "nonce": nonce,
            "customize_changeset_status": "publish",
            "customized": customized,
        },
        timeout=30,
    )

    if resp.status_code == 200:
        try:
            result = resp.json()
            if result.get("success"):
                print(f"  [OK] CSS 저장 완료! ({len(CUSTOM_CSS)} bytes → {theme})")
                return True
            else:
                print(f"  [ERR] 저장 실패: {json.dumps(result, ensure_ascii=False)[:300]}")
        except Exception:
            print(f"  [ERR] 응답 파싱 실패: {resp.text[:300]}")
    else:
        print(f"  [ERR] HTTP {resp.status_code}: {resp.text[:300]}")

    return False


def main():
    print(f"=== WordPress Customizer CSS 자동 주입 ===")
    print(f"  사이트: {WP_URL}")
    print(f"  사용자: {WP_USER}")

    if not step1_login():
        print("\n로그인 실패. WP_LOGIN_PASSWORD를 확인해주세요.")
        sys.exit(1)

    result = step2_get_nonce()
    if len(result) != 3:
        print("\nnonce 추출 실패.")
        sys.exit(1)

    nonce, theme, changeset_uuid = result

    if step3_save_css(nonce, theme, changeset_uuid):
        print(f"\n=== 완료! {domain}에 CSS 적용됨 ===")
    else:
        print(f"\n=== CSS 저장 실패 — 수동 적용 필요 ===")
        print(f"  {WP_URL}/wp-admin/customize.php → 추가 CSS")
        sys.exit(1)


if __name__ == "__main__":
    main()
