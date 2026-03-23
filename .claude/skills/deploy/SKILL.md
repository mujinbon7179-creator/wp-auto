---
name: deploy
description: Vercel 배포, GitHub Push, 환경변수 설정 등 배포 관련 작업에 적용.
---

# 배포 가이드

## Git 워크플로우
```bash
git add .
git commit -m "feat: 변경 설명"
git push
```
- Vercel은 main 브랜치 push 시 자동 배포
- 커밋 메시지: conventional commits (feat:, fix:, chore:, refactor:)

## Vercel 환경변수
- NEXT_PUBLIC_SUPABASE_URL
- NEXT_PUBLIC_SUPABASE_ANON_KEY
- Vercel Dashboard → Settings → Environment Variables

## GitHub Actions
- .github/workflows/publish.yml
- Secrets: Settings → Secrets and variables → Actions
- 수동 실행: Actions → Run workflow

## 빌드 확인
```bash
npm run build  # 에러 없어야 Push
```
