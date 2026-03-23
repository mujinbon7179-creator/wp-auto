---
name: dashboard-redesign
description: AutoBlog 대시보드 UI 리디자인 시 사용. 디자인 변경, 컴포넌트 추가, 스타일링 작업에 자동 적용.
---

# 대시보드 리디자인 가이드

## 디자인 원칙
- 라이트 모드 기본 (밝고 온화한 톤)
- 배경: #FAFBFC, 카드: #FFFFFF
- 주 색상: #6366F1 (인디고), 보조: #8B5CF6 (퍼플)
- 성공: #10B981, 경고: #F59E0B, 위험: #EF4444
- 폰트: system-ui, 한국어 최적화
- 카드: border-radius: 16px, box-shadow: 0 1px 3px rgba(0,0,0,0.08)
- 여백: 충분히, padding 20~24px

## 필수 모듈 (v3 기준 9개)
1. 개요 (KPI 카드 + 발행 추이 차트)
2. 발행 로그 (테이블 + 필터)
3. 수익 (채널별 + 일별 추이)
4. 비용 (모델별 + 파이차트)
5. SEO (인덱싱 현황 + 키워드)
6. 이메일 (구독자 + 전환율)
7. SNS (플랫폼별 성과)
8. 알림 (실시간 + 읽음 처리)
9. 설정 (사이트 관리 + AI 모델 선택)

## AI 모델 설정 패널 (설정 탭)
- 초안 모델: Grok / Gemini / GPT-5 mini / DeepSeek (드롭다운)
- 폴리싱: ON/OFF 토글
- 폴리싱 모델: Claude Sonnet / Claude Haiku / 없음
- 편당 예상 비용 실시간 표시
- 설정 → Supabase dashboard_config 테이블에 저장

## 차트 라이브러리
- Recharts 사용
- 라이트 모드 색상 적용
- 툴팁: 흰색 배경, 그림자

## 파일 경로
- 메인: src/app/page.js
- 훅: src/lib/hooks.js
- 스타일: src/app/globals.css
