# AutoBlog Engine — Installation Guide

> 30분 내 설치 완료. WordPress 사이트와 AI 기반 자동 블로그를 연결합니다.

---

## Prerequisites

- WordPress 사이트 (자체 도메인 + HTTPS)
- GitHub 계정
- Vercel 계정 (무료)
- Supabase 계정 (무료)
- AI API 키 1개 이상 (DeepSeek 권장 — 가성비 최고)

---

## Step 1: GitHub Repository

1. 이 저장소 우측 상단 **"Use this template"** > **"Create a new repository"**
2. Repository name: `wp-auto` (비공개 권장)
3. **Create repository**

---

## Step 2: Supabase Setup

1. [supabase.com](https://supabase.com) 에서 새 프로젝트 생성
2. SQL Editor에서 마이그레이션 실행 (순서대로):

```
migrations/001_consumer_dashboard.sql
migrations/002_admin_role.sql
migrations/003_auto_admin_first_user.sql
```

3. **Project Settings > API** 에서 확인:
   - `Project URL` → NEXT_PUBLIC_SUPABASE_URL
   - `anon public` key → NEXT_PUBLIC_SUPABASE_ANON_KEY
   - `service_role` key → SUPABASE_SERVICE_KEY

4. **Authentication > URL Configuration**:
   - Site URL: `https://your-domain.com`
   - Redirect URLs: `https://your-domain.com/**`

---

## Step 3: Vercel Deployment

1. [vercel.com](https://vercel.com) > **Add New Project** > GitHub 연결 > `wp-auto` 선택
2. Environment Variables 설정:

| Variable | Value | Required |
|----------|-------|----------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase Project URL | Yes |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key | Yes |
| `SUPABASE_SERVICE_KEY` | Supabase service_role key | Yes |
| `GITHUB_TOKEN` | GitHub PAT (repo + workflow) | Yes |
| `GITHUB_REPO` | `your-username/wp-auto` | Yes |

3. **Deploy** 클릭
4. 커스텀 도메인 연결 (Settings > Domains)

---

## Step 4: GitHub Secrets

fork한 저장소 > **Settings > Secrets and variables > Actions** 에서 추가:

### Required

| Secret | Description |
|--------|-------------|
| `SUPABASE_URL` | Supabase Project URL |
| `SUPABASE_KEY` | Supabase service_role key |
| `DEEPSEEK_API_KEY` | DeepSeek API key |

### Optional (Recommended)

| Secret | Description |
|--------|-------------|
| `CLAUDE_API_KEY` | Claude API key (고품질 폴리싱) |
| `GROK_API_KEY` | Grok API key (보조 모델) |
| `GEMINI_API_KEY` | Gemini API key (보조 모델) |
| `UNSPLASH_ACCESS_KEY` | Unsplash API (이미지) |
| `PEXELS_API_KEY` | Pexels API (이미지) |
| `PIXABAY_API_KEY` | Pixabay API (이미지) |

---

## Step 5: WordPress Setup

1. WordPress 관리자 로그인
2. **사용자 > 프로필 > 앱 비밀번호** 에서 새 앱 비밀번호 생성
3. 대시보드 접속 (your-domain.com)
4. 회원가입 (첫 가입 유저 = 자동 관리자)
5. **설정 > STEP 1** 에서 WordPress URL + 앱 비밀번호 입력
6. **STEP 2 > 블로그 시작하기** 클릭

---

## Verification

설정 완료 후 확인:

- [ ] 대시보드 접속 정상 (your-domain.com)
- [ ] 설정 페이지에서 시스템 상태 체크 통과 (빨간 경고 없음)
- [ ] "블로그 시작하기" 후 WordPress에 글 게시 확인
- [ ] GitHub Actions 탭에서 `publish.yml` 실행 성공 확인

---

## Scheduled Publishing

설치 완료 후 GitHub Actions가 하루 4회 (KST 07/12/17/22시) 자동 실행됩니다.
대시보드 설정에서 발행 횟수와 시간을 변경할 수 있습니다.

---

## Troubleshooting

| 문제 | 해결 |
|------|------|
| "GITHUB_TOKEN이 설정되지 않았습니다" | Vercel 환경변수에 GITHUB_TOKEN 추가 |
| "GitHub API failed: 404" | GITHUB_REPO를 본인 저장소로 변경 (`your-username/wp-auto`) |
| WordPress 연결 실패 | HTTPS 확인 + 앱 비밀번호 재생성 |
| 글이 발행되지 않음 | GitHub Actions 탭에서 로그 확인 → API 키 누락 체크 |
