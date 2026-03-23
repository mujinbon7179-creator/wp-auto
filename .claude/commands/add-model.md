발행 엔진에 새 AI 모델을 추가합니다.

사용자에게 물어볼 것:
1. 모델 이름 (예: gpt-5-mini)
2. API 엔드포인트 URL
3. 인증 방식 (Bearer token / API key)
4. 가격 (input/output per 1M tokens)
5. 폴백 체인 내 위치 (1차/2차/3차/백업)

작업:
1. scripts/main.py에 _call_모델명() 메서드 추가
2. COST_RATES에 가격 추가
3. generate() 폴백 체인 업데이트
4. .github/workflows/publish.yml에 환경변수 추가
5. python scripts/main.py --dry-run --count 1로 테스트
