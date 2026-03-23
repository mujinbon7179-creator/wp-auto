---
name: engine-dev
description: AutoBlog 발행 엔진 개발/수정 시 사용. Python 코드, AI 모델 라우팅, WordPress API 작업에 적용.
---

# 발행 엔진 개발 가이드

## 아키텍처
```
scripts/main.py
├── KeywordManager    — 키워드 선택/사용 추적
├── ContentGenerator  — 멀티모델 AI 글 생성
│   ├── Grok (1차 초안)
│   ├── Gemini (2차 폴백)
│   ├── DeepSeek (3차 백업)
│   └── Claude Sonnet (폴리싱)
├── ImageManager      — Unsplash 이미지
├── AffiliateManager  — 제휴 링크 삽입
├── WordPressPublisher — WP REST API 발행
└── SupabaseLogger    — 대시보드 로깅
```

## 모델 추가 시 체크리스트
1. 환경변수 추가 (os.environ.get)
2. _call_모델명() 메서드 작성
3. COST_RATES에 가격 추가
4. generate() 폴백 체인에 삽입
5. publish.yml에 env 추가
6. README.md 업데이트

## WordPress REST API
- 엔드포인트: {WP_URL}/wp-json/wp/v2/posts
- 인증: Basic Auth (base64)
- 카테고리/태그: 없으면 자동 생성

## 테스트
```bash
python scripts/main.py --count 1 --dry-run  # 발행 없이 테스트
python scripts/main.py --count 1             # 실제 1편 발행
```
