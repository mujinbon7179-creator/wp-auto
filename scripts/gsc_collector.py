#!/usr/bin/env python3
"""
Google Search Console 데이터 수집기
- 일 1회 실행하여 seo_health 테이블에 검색 성과 기록
- 7일 이상 미인덱싱 글 경고 알림 발생
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta, timezone

import requests

# ── 환경 변수 ──
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
SITE_ID = os.environ.get("SITE_ID", "")
GSC_CREDENTIALS_JSON = os.environ.get("GSC_CREDENTIALS_JSON", "")
GSC_SITE_URL = os.environ.get("GSC_SITE_URL", "")  # e.g. "https://planx-ai.com/"

KST = timezone(timedelta(hours=9))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("gsc_collector")


def get_gsc_service():
    """Google Search Console API 서비스 객체 생성 (서비스 계정 인증)"""
    if not GSC_CREDENTIALS_JSON:
        log.error("GSC_CREDENTIALS_JSON 환경변수 미설정")
        return None

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds_data = json.loads(GSC_CREDENTIALS_JSON)
        credentials = service_account.Credentials.from_service_account_info(
            creds_data,
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
        )
        service = build("searchconsole", "v1", credentials=credentials)
        return service
    except ImportError:
        log.error("google-auth / google-api-python-client 미설치. pip install google-auth google-api-python-client")
        return None
    except Exception as e:
        log.error(f"GSC 서비스 생성 실패: {e}")
        return None


def fetch_gsc_data(service, site_url, date_str):
    """GSC에서 특정 날짜의 검색 성과 데이터 조회"""
    try:
        response = service.searchanalytics().query(
            siteUrl=site_url,
            body={
                "startDate": date_str,
                "endDate": date_str,
                "dimensions": ["query"],
                "rowLimit": 50
            }
        ).execute()

        rows = response.get("rows", [])
        total_clicks = sum(r.get("clicks", 0) for r in rows)
        total_impressions = sum(r.get("impressions", 0) for r in rows)
        avg_position = (
            sum(r.get("position", 0) * r.get("impressions", 1) for r in rows)
            / max(total_impressions, 1)
        ) if rows else None

        top_keywords = [
            {"query": r["keys"][0], "clicks": r.get("clicks", 0),
             "impressions": r.get("impressions", 0), "position": round(r.get("position", 0), 1)}
            for r in sorted(rows, key=lambda x: x.get("clicks", 0), reverse=True)[:10]
        ]

        return {
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "avg_position": round(avg_position, 1) if avg_position else None,
            "top_keywords": top_keywords
        }
    except Exception as e:
        log.error(f"GSC 데이터 조회 실패: {e}")
        return None


def fetch_indexed_pages(service, site_url):
    """GSC URL 검사 API로 인덱싱 상태 확인 (사이트맵 기반)"""
    try:
        sitemaps = service.sitemaps().list(siteUrl=site_url).execute()
        sitemap_list = sitemaps.get("sitemap", [])
        total_submitted = 0
        total_indexed = 0
        for sm in sitemap_list:
            for content_info in sm.get("contents", []):
                total_submitted += content_info.get("submitted", 0)
                total_indexed += content_info.get("indexed", 0)
        return total_submitted, total_indexed
    except Exception as e:
        log.warning(f"사이트맵 인덱싱 정보 조회 실패: {e}")
        return 0, 0


def save_to_supabase(data):
    """seo_health 테이블에 upsert"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        log.error("Supabase 환경변수 미설정")
        return False

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    try:
        resp = requests.post(
            f"{SUPABASE_URL}/rest/v1/seo_health",
            headers=headers,
            json=data,
            timeout=15
        )
        resp.raise_for_status()
        log.info(f"seo_health 저장 완료: {data['date']}")
        return True
    except Exception as e:
        log.error(f"Supabase 저장 실패: {e}")
        return False


def check_unindexed_posts():
    """7일 이상 발행됐지만 인덱싱 안 된 글 찾아 경고"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }

    seven_days_ago = (datetime.now(KST) - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00")

    try:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/publish_logs",
            headers=headers,
            params={
                "select": "id,title,keyword,url,created_at",
                "status": "eq.published",
                "seo_indexed": "eq.false",
                "created_at": f"lt.{seven_days_ago}",
                "site_id": f"eq.{SITE_ID}",
                "limit": "20"
            },
            timeout=15
        )
        resp.raise_for_status()
        unindexed = resp.json()

        if unindexed:
            log.warning(f"7일+ 미인덱싱 글 {len(unindexed)}건 발견")
            alert_msg = "; ".join(
                f"'{p['title'][:30]}' ({p.get('keyword', '')})"
                for p in unindexed[:5]
            )

            alert_headers = {**headers, "Content-Type": "application/json", "Prefer": "return=minimal"}
            requests.post(
                f"{SUPABASE_URL}/rest/v1/alerts",
                headers=alert_headers,
                json={
                    "site_id": SITE_ID,
                    "title": f"미인덱싱 경고: {len(unindexed)}건",
                    "message": f"7일 이상 미인덱싱: {alert_msg}",
                    "severity": "warning",
                    "category": "seo_unindexed"
                },
                timeout=10
            )
        else:
            log.info("미인덱싱 경고 없음")

    except Exception as e:
        log.error(f"미인덱싱 체크 실패: {e}")


def main():
    log.info("=== GSC 데이터 수집 시작 ===")

    service = get_gsc_service()
    if not service:
        log.error("GSC 서비스 초기화 실패 — 종료")
        sys.exit(1)

    if not GSC_SITE_URL:
        log.error("GSC_SITE_URL 미설정 — 종료")
        sys.exit(1)

    # GSC 데이터는 2-3일 지연됨 → 3일 전 데이터 수집
    target_date = (datetime.now(KST) - timedelta(days=3)).strftime("%Y-%m-%d")
    log.info(f"수집 대상 날짜: {target_date}")

    # 검색 성과 데이터
    gsc_data = fetch_gsc_data(service, GSC_SITE_URL, target_date)
    if not gsc_data:
        log.error("GSC 데이터 수집 실패")
        sys.exit(1)

    # 인덱싱 현황 (사이트맵 기반)
    total_posts, indexed_posts = fetch_indexed_pages(service, GSC_SITE_URL)
    indexing_rate = round((indexed_posts / max(total_posts, 1)) * 100, 1)

    # Supabase 저장
    record = {
        "site_id": SITE_ID,
        "date": target_date,
        "total_posts": total_posts,
        "indexed_posts": indexed_posts,
        "indexing_rate": indexing_rate,
        "avg_position": gsc_data["avg_position"],
        "total_impressions": gsc_data["total_impressions"],
        "total_clicks": gsc_data["total_clicks"],
        "top_keywords": json.dumps(gsc_data["top_keywords"], ensure_ascii=False),
    }

    save_to_supabase(record)

    log.info(f"  인덱싱: {indexed_posts}/{total_posts} ({indexing_rate}%)")
    log.info(f"  클릭: {gsc_data['total_clicks']}, 노출: {gsc_data['total_impressions']}")
    log.info(f"  평균순위: {gsc_data['avg_position']}")

    # 미인덱싱 경고 체크
    check_unindexed_posts()

    log.info("=== GSC 데이터 수집 완료 ===")


if __name__ == "__main__":
    main()
