#!/usr/bin/env python3
"""
WordPress 글별 통계 수집기
- WP REST API로 글 목록 + 조회수(Jetpack/WP-Statistics) 수집
- publish_logs에 조회수/성과 데이터 업데이트
- 대시보드용 성과 요약 생성
"""

import os
import sys
import json
import base64
import logging
from datetime import datetime, timedelta, timezone

import requests

# ── 환경 변수 ──
WP_URL = os.environ.get("WP_URL", "").rstrip("/")
WP_USER = os.environ.get("WP_USERNAME", "")
WP_PASS = os.environ.get("WP_APP_PASSWORD", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
SITE_ID = os.environ.get("SITE_ID", "")

KST = timezone(timedelta(hours=9))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("wp_stats")


def get_wp_headers():
    """WordPress REST API 인증 헤더"""
    if WP_URL.endswith("/wp-json/wp/v2"):
        base_url = WP_URL[:-len("/wp-json/wp/v2")]
    else:
        base_url = WP_URL
    cred = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
    return base_url, {"Authorization": f"Basic {cred}"}


def fetch_wp_posts(base_url, headers, per_page=100, page=1):
    """WP REST API로 발행된 글 목록 조회"""
    try:
        resp = requests.get(
            f"{base_url}/wp-json/wp/v2/posts",
            headers=headers,
            params={
                "per_page": per_page,
                "page": page,
                "status": "publish",
                "_fields": "id,title,link,date,slug,meta"
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        log.error(f"WP 글 목록 조회 실패: {e}")
        return []


def fetch_post_views_jetpack(base_url, headers, post_id):
    """Jetpack Stats API로 개별 글 조회수 (Jetpack 설치 시)"""
    try:
        resp = requests.get(
            f"{base_url}/wp-json/wpcom/v2/stats/post/{post_id}",
            headers=headers,
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("views", 0)
    except Exception:
        pass
    return None


def fetch_post_views_wp_statistics(base_url, headers, post_id):
    """WP-Statistics 플러그인 API로 조회수 (WP-Statistics 설치 시)"""
    try:
        resp = requests.get(
            f"{base_url}/wp-json/wp-statistics/v2/hits",
            headers=headers,
            params={"post_id": post_id},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("total", 0)
    except Exception:
        pass
    return None


def fetch_post_views(base_url, headers, post_id):
    """조회수 수집 — Jetpack → WP-Statistics → post meta 순으로 폴백"""
    views = fetch_post_views_jetpack(base_url, headers, post_id)
    if views is not None:
        return views, "jetpack"

    views = fetch_post_views_wp_statistics(base_url, headers, post_id)
    if views is not None:
        return views, "wp-statistics"

    # post meta에서 views 필드 체크 (일부 테마/플러그인)
    try:
        resp = requests.get(
            f"{base_url}/wp-json/wp/v2/posts/{post_id}",
            headers=headers,
            params={"_fields": "meta"},
            timeout=10
        )
        if resp.status_code == 200:
            meta = resp.json().get("meta", {})
            for key in ["views", "post_views_count", "_views"]:
                if key in meta and meta[key]:
                    return int(meta[key]), "post_meta"
    except Exception:
        pass

    return 0, "unavailable"


def update_publish_logs(post_stats):
    """publish_logs에 조회수 데이터 업데이트"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        log.error("Supabase 환경변수 미설정")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    updated = 0
    for stat in post_stats:
        try:
            # URL 기준으로 publish_logs 매칭 → views 업데이트
            resp = requests.patch(
                f"{SUPABASE_URL}/rest/v1/publish_logs",
                headers=headers,
                params={
                    "url": f"eq.{stat['url']}",
                    "site_id": f"eq.{SITE_ID}"
                },
                json={
                    "views": stat["views"],
                    "views_source": stat["source"],
                    "views_updated_at": datetime.now(KST).isoformat()
                },
                timeout=10
            )
            if resp.status_code in (200, 204):
                updated += 1
        except Exception as e:
            log.warning(f"조회수 업데이트 실패 ({stat['url']}): {e}")

    log.info(f"publish_logs 업데이트: {updated}/{len(post_stats)}건")


def generate_performance_summary(post_stats):
    """성과 요약 생성 → alerts 테이블에 기록"""
    if not post_stats:
        return

    total_views = sum(s["views"] for s in post_stats)
    top_posts = sorted(post_stats, key=lambda x: x["views"], reverse=True)[:5]
    zero_views = [s for s in post_stats if s["views"] == 0 and s.get("age_days", 0) >= 7]

    summary_parts = [
        f"총 조회수: {total_views:,}",
        f"수집 글: {len(post_stats)}건",
    ]

    if top_posts and top_posts[0]["views"] > 0:
        summary_parts.append(
            f"Top 1: '{top_posts[0]['title'][:30]}' ({top_posts[0]['views']:,}뷰)"
        )

    if zero_views:
        summary_parts.append(f"7일+ 조회수 0: {len(zero_views)}건 (SEO 점검 필요)")

    summary = " | ".join(summary_parts)
    log.info(f"성과 요약: {summary}")

    if zero_views and SUPABASE_URL and SUPABASE_KEY:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        try:
            requests.post(
                f"{SUPABASE_URL}/rest/v1/alerts",
                headers=headers,
                json={
                    "site_id": SITE_ID,
                    "title": f"조회수 0 경고: {len(zero_views)}건",
                    "message": summary,
                    "severity": "info",
                    "category": "performance_low"
                },
                timeout=10
            )
        except Exception:
            pass


def main():
    log.info("=== WordPress 통계 수집 시작 ===")

    if not WP_URL or not WP_USER or not WP_PASS:
        log.error("WordPress 환경변수 미설정 (WP_URL, WP_USERNAME, WP_APP_PASSWORD)")
        sys.exit(1)

    base_url, headers = get_wp_headers()

    # 최근 100개 글 조회
    posts = fetch_wp_posts(base_url, headers, per_page=100)
    if not posts:
        log.warning("발행된 글 없음")
        sys.exit(0)

    log.info(f"WordPress 글 {len(posts)}개 조회됨")

    # 글별 조회수 수집
    post_stats = []
    source_detected = None

    for post in posts:
        post_id = post["id"]
        title = post.get("title", {}).get("rendered", "")
        url = post.get("link", "")
        pub_date = post.get("date", "")

        views, source = fetch_post_views(base_url, headers, post_id)
        if source_detected is None and source != "unavailable":
            source_detected = source
            log.info(f"조회수 소스 감지: {source}")

        age_days = 0
        if pub_date:
            try:
                pub_dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
                age_days = (datetime.now(timezone.utc) - pub_dt).days
            except Exception:
                pass

        post_stats.append({
            "post_id": post_id,
            "title": title,
            "url": url,
            "views": views,
            "source": source,
            "age_days": age_days,
        })

    if source_detected:
        log.info(f"조회수 소스: {source_detected}")
    else:
        log.warning("조회수 수집 불가 — Jetpack 또는 WP-Statistics 플러그인 필요")

    # Supabase에 조회수 업데이트
    stats_with_views = [s for s in post_stats if s["source"] != "unavailable"]
    if stats_with_views:
        update_publish_logs(stats_with_views)

    # 성과 요약
    generate_performance_summary(post_stats)

    log.info("=== WordPress 통계 수집 완료 ===")


if __name__ == "__main__":
    main()
