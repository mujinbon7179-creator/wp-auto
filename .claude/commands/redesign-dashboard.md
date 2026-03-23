대시보드를 리디자인합니다.

요구사항:
1. src/app/page.js를 수정하여 v3 디자인 9개 모듈 전체 적용
2. 라이트 모드 (밝고 온화한 톤 + 고급스러운 UI)
3. AI 모델 설정 패널 추가 (설정 탭)
4. Supabase 실시간 연동 유지
5. Recharts 차트 스타일 라이트 모드 적용

작업 순서:
1. src/app/globals.css 라이트 모드 CSS 변수 적용
2. src/app/page.js 전체 리디자인
3. src/lib/hooks.js 필요 시 훅 추가
4. npm run build로 빌드 확인
5. git push로 Vercel 자동 배포
