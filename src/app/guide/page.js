'use client';
import { useState } from 'react';
import { isCentral } from '@/lib/instance';
import { Card, ActionButton } from '@/components/ui';

// ── Central (SaaS) Guide Steps ──

const CENTRAL_STEPS = [
  { id: 'hosting', title: 'WordPress 준비', icon: '1', content: CentralHostingStep },
  { id: 'app-password', title: '앱 비밀번호 생성', icon: '2', content: CentralAppPasswordStep },
  { id: 'signup', title: '회원가입', icon: '3', content: CentralSignupStep },
  { id: 'setup', title: '블로그 설정', icon: '4', content: CentralSetupStep },
  { id: 'monetization', title: '수익화', icon: '5', content: CentralMonetizationStep },
  { id: 'faq', title: 'FAQ', icon: '?', content: CentralFaqStep },
];

// ── Self-hosted Guide Steps ──

const SELFHOST_STEPS = [
  { id: 'overview', title: '개요 + 준비물', icon: '1', content: SelfhostOverviewStep },
  { id: 'wordpress', title: 'WordPress 호스팅', icon: '2', content: SelfhostWordPressStep },
  { id: 'github', title: 'GitHub Fork', icon: '3', content: SelfhostGithubStep },
  { id: 'api-keys', title: 'AI API 키 발급', icon: '4', content: SelfhostApiKeysStep },
  { id: 'supabase', title: 'Supabase 프로젝트', icon: '5', content: SelfhostSupabaseStep },
  { id: 'vercel', title: 'Vercel 배포', icon: '6', content: SelfhostVercelStep },
  { id: 'secrets', title: 'GitHub Secrets', icon: '7', content: SelfhostSecretsStep },
  { id: 'first-run', title: '첫 실행', icon: '8', content: SelfhostFirstRunStep },
  { id: 'daily', title: '운영 + 수익화', icon: '9', content: SelfhostDailyStep },
];

export default function GuidePage() {
  const central = isCentral();
  const STEPS = central ? CENTRAL_STEPS : SELFHOST_STEPS;
  const [currentStep, setCurrentStep] = useState(0);
  const StepContent = STEPS[currentStep].content;

  return (
    <div style={{ maxWidth: 900, margin: '0 auto', padding: '24px 16px' }}>
      <h1 style={{ fontSize: 24, fontWeight: 800, marginBottom: 4 }}>
        {central ? '시작 가이드' : '셀프 호스팅 설치 가이드'}
      </h1>
      <p style={{ fontSize: 13, color: 'var(--text-dim)', marginBottom: 24 }}>
        {central
          ? '10분이면 AI 자동 블로그가 시작됩니다.'
          : '30분 내 나만의 AI 블로그 시스템을 구축합니다.'}
      </p>

      <div style={{ display: 'flex', gap: 24 }}>
        {/* Step sidebar */}
        <div style={{ width: 220, flexShrink: 0 }}>
          {STEPS.map((step, i) => (
            <button key={step.id} onClick={() => setCurrentStep(i)} style={{
              display: 'flex', alignItems: 'center', gap: 10,
              width: '100%', padding: '10px 12px', marginBottom: 4, borderRadius: 10,
              border: 'none', cursor: 'pointer', textAlign: 'left',
              background: currentStep === i ? 'var(--accent-bg)' : 'transparent',
              color: currentStep === i ? 'var(--accent)' : 'var(--text-secondary)',
              fontWeight: currentStep === i ? 700 : 400, fontSize: 13,
              transition: 'all 0.2s',
            }}>
              <span style={{
                width: 26, height: 26, borderRadius: 13, flexShrink: 0,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 12, fontWeight: 700,
                background: i < currentStep ? 'var(--green)' : currentStep === i ? 'var(--accent)' : 'var(--border-light)',
                color: i <= currentStep ? '#fff' : 'var(--text-dim)',
              }}>
                {i < currentStep ? '\u2713' : step.icon}
              </span>
              {step.title}
            </button>
          ))}
        </div>

        {/* Step content */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <Card style={{ padding: '24px 28px' }}>
            <StepContent />
          </Card>

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 16 }}>
            <ActionButton variant="ghost" onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
              disabled={currentStep === 0} style={{ fontSize: 13 }}>
              &larr; 이전
            </ActionButton>
            <ActionButton onClick={() => setCurrentStep(Math.min(STEPS.length - 1, currentStep + 1))}
              disabled={currentStep === STEPS.length - 1} style={{ fontSize: 13 }}>
              다음 &rarr;
            </ActionButton>
          </div>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════
// Central (SaaS) Steps
// ══════════════════════════════════════

function CentralHostingStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>WordPress 사이트 준비</h2>
    <p>자동 발행을 위해 WordPress 사이트가 필요합니다.</p>
    <div style={S.box}>
      <strong>필요 조건:</strong>
      <ul style={S.ul}>
        <li>자체 도메인 + HTTPS 적용된 WordPress 사이트</li>
        <li>관리자(wp-admin) 접근 가능</li>
        <li>REST API 활성화 (기본값)</li>
      </ul>
    </div>
    <div style={S.tip}>아직 WordPress가 없다면 <a href="https://www.cloudways.com" target="_blank" rel="noopener" style={S.link}>Cloudways</a>를 추천합니다. 월 $14부터 시작.</div>
  </div>);
}

function CentralAppPasswordStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>앱 비밀번호 생성</h2>
    <p>AutoBlog이 WordPress에 글을 발행하려면 앱 비밀번호가 필요합니다.</p>
    <ol style={S.ol}>
      <li>WordPress 관리자 페이지 접속 (yoursite.com/wp-admin)</li>
      <li>좌측 <strong>사용자 &rarr; 프로필</strong></li>
      <li>페이지 하단 <strong>"앱 비밀번호"</strong> 섹션</li>
      <li>이름 입력 (예: "AutoBlog") &rarr; <strong>"새 앱 비밀번호 추가"</strong></li>
      <li>생성된 비밀번호 복사 (공백 포함 전체)</li>
    </ol>
    <div style={S.warn}>앱 비밀번호가 보이지 않으면 HTTPS가 필요합니다. 또는 "Application Passwords" 플러그인을 설치하세요.</div>
  </div>);
}

function CentralSignupStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>회원가입</h2>
    <p>대시보드에서 회원가입하면 바로 시작할 수 있습니다.</p>
    <div style={S.box}>
      <ol style={S.ol}>
        <li><a href="/login" style={S.link}>로그인 페이지</a>에서 "회원가입" 탭 클릭</li>
        <li>이름, 이메일, 비밀번호 입력</li>
        <li>이메일 인증 완료 (메일함 확인)</li>
      </ol>
    </div>
  </div>);
}

function CentralSetupStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>블로그 설정</h2>
    <p><a href="/settings" style={S.link}>설정 페이지</a>에서 2단계로 완료합니다.</p>
    <div style={S.box}>
      <strong>Step 1 — 사이트 연결</strong>
      <ul style={S.ul}>
        <li>WordPress URL 입력</li>
        <li>앱 비밀번호 입력</li>
        <li>"연결 테스트" &rarr; "사이트 등록"</li>
      </ul>
    </div>
    <div style={{ ...S.box, marginTop: 12 }}>
      <strong>Step 2 — 블로그 설정</strong>
      <ul style={S.ul}>
        <li>니치(주제) 2개 이상 선택</li>
        <li>운영자명 + 이메일 입력</li>
        <li>발행 스케줄 설정</li>
        <li><strong>"블로그 시작하기"</strong> 클릭 &rarr; 자동 초기화!</li>
      </ul>
    </div>
  </div>);
}

function CentralMonetizationStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>수익화 로드맵</h2>
    <div style={S.box}>
      <strong>Stage 1: AdSense 승인 준비</strong> (글 30개+)
      <ul style={S.ul}>
        <li>고품질 글만 자동 발행 (85점+)</li>
        <li>제휴 링크 없음 — 순수 정보성 콘텐츠</li>
        <li>약 2~4주 후 Google AdSense 신청</li>
      </ul>
    </div>
    <div style={{ ...S.box, marginTop: 12 }}>
      <strong>Stage 2: 수익화 시작</strong> (AdSense 승인 후)
      <ul style={S.ul}>
        <li>설정에서 Stage 2로 전환</li>
        <li>쿠팡 파트너스 딥링크 등록</li>
        <li>텐핑 CPA 캠페인 등록</li>
        <li>글에 자동 삽입 시작</li>
      </ul>
    </div>
  </div>);
}

function CentralFaqStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>자주 묻는 질문</h2>
    {[
      { q: '하루에 몇 편까지 발행되나요?', a: '설정에서 1~5회까지 조절 가능합니다. 기본 2회.' },
      { q: '글 내용을 수정할 수 있나요?', a: '네. WordPress 관리자(wp-admin)에서 직접 수정 가능합니다.' },
      { q: 'AI가 작성한 글의 품질은?', a: '품질 점수 85점+ 기준을 통과한 글만 발행됩니다. 미달 시 자동 재생성.' },
      { q: 'AdSense 승인까지 얼마나 걸리나요?', a: '보통 글 30개 이상 + 2~4주 소요. Stage 1 모드가 승인에 최적화되어 있습니다.' },
    ].map((item, i) => (
      <div key={i} style={{ marginBottom: 16 }}>
        <div style={{ fontSize: 14, fontWeight: 700, color: 'var(--text)' }}>{item.q}</div>
        <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 4 }}>{item.a}</div>
      </div>
    ))}
  </div>);
}

// ══════════════════════════════════════
// Self-hosted Steps
// ══════════════════════════════════════

function SelfhostOverviewStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>나만의 AI 블로그 시스템</h2>
    <p>이 가이드를 따라하면 30분 내에 AI가 자동으로 블로그 글을 작성하고 발행하는 시스템을 구축합니다.</p>
    <div style={S.box}>
      <strong>준비물:</strong>
      <ul style={S.ul}>
        <li>WordPress 사이트 (자체 도메인 + HTTPS)</li>
        <li>GitHub 계정 (무료)</li>
        <li>Vercel 계정 (무료)</li>
        <li>Supabase 계정 (무료)</li>
        <li>AI API 키 1개 (DeepSeek 권장 — 월 $2~5)</li>
      </ul>
    </div>
    <div style={S.box}>
      <strong>구조:</strong>
      <ul style={S.ul}>
        <li><strong>GitHub</strong>: AI 발행 엔진 (하루 4회 자동 실행)</li>
        <li><strong>Vercel</strong>: 대시보드 웹사이트</li>
        <li><strong>Supabase</strong>: 데이터베이스 (발행 기록, 설정)</li>
        <li><strong>WordPress</strong>: 블로그 (글이 여기에 발행됨)</li>
      </ul>
    </div>
  </div>);
}

function SelfhostWordPressStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>WordPress 호스팅</h2>
    <p>아직 WordPress가 없다면 호스팅 서비스에서 설치하세요.</p>
    <div style={S.box}>
      <strong>추천: <a href="https://www.cloudways.com" target="_blank" rel="noopener" style={S.link}>Cloudways</a></strong> (월 $14~)
      <ul style={S.ul}>
        <li>서버 생성 (DigitalOcean, 싱가포르 리전)</li>
        <li>Application에서 WordPress 선택</li>
        <li>도메인 연결 + SSL 인증서 적용</li>
      </ul>
    </div>
    <div style={S.box}>
      <strong>앱 비밀번호 생성:</strong>
      <ol style={S.ol}>
        <li>WordPress 관리자 접속 (yoursite.com/wp-admin)</li>
        <li>사용자 &rarr; 프로필 &rarr; 하단 "앱 비밀번호"</li>
        <li>이름: "AutoBlog" &rarr; 새 앱 비밀번호 추가</li>
        <li>생성된 비밀번호 메모 (나중에 사용)</li>
      </ol>
    </div>
  </div>);
}

function SelfhostGithubStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>GitHub 저장소 Fork</h2>
    <ol style={S.ol}>
      <li>아래 링크를 클릭하여 저장소를 Fork합니다</li>
    </ol>
    <a href="https://github.com/planxs-ai/wp-auto/fork" target="_blank" rel="noopener" style={S.bigBtn}>
      GitHub에서 Fork하기 &rarr;
    </a>
    <ol start={2} style={S.ol}>
      <li>Repository name: <code style={S.code}>wp-auto</code> (그대로)</li>
      <li><strong>Create fork</strong> 클릭</li>
      <li>Fork된 저장소 &rarr; <strong>Settings &rarr; Actions &rarr; General</strong></li>
      <li>"Allow all actions" 선택 &rarr; <strong>Save</strong></li>
    </ol>
    <div style={S.tip}>Fork한 저장소의 Actions 탭이 비활성화되어 있으면 "I understand my workflows, go ahead and enable them"을 클릭하세요.</div>
  </div>);
}

function SelfhostApiKeysStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>AI API 키 발급</h2>
    <p>최소 1개의 AI API 키가 필요합니다. DeepSeek이 가장 저렴합니다.</p>
    <div style={S.box}>
      <strong>필수 (1개 선택):</strong>
      <ul style={S.ul}>
        <li><a href="https://platform.deepseek.com/api_keys" target="_blank" rel="noopener" style={S.link}>DeepSeek</a> — 가성비 최고 (월 $2~5)</li>
        <li><a href="https://aistudio.google.com/apikey" target="_blank" rel="noopener" style={S.link}>Google Gemini</a> — 무료 티어 있음</li>
      </ul>
    </div>
    <div style={S.box}>
      <strong>선택 (품질 향상):</strong>
      <ul style={S.ul}>
        <li><a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener" style={S.link}>Claude API</a> — 폴리싱용 (고품질)</li>
        <li><a href="https://console.x.ai" target="_blank" rel="noopener" style={S.link}>Grok API</a> — 보조 모델</li>
      </ul>
    </div>
    <div style={S.box}>
      <strong>이미지 API (선택):</strong>
      <ul style={S.ul}>
        <li><a href="https://unsplash.com/developers" target="_blank" rel="noopener" style={S.link}>Unsplash</a></li>
        <li><a href="https://www.pexels.com/api/" target="_blank" rel="noopener" style={S.link}>Pexels</a></li>
      </ul>
    </div>
    <div style={S.tip}>API 키를 메모해두세요. Step 7에서 GitHub Secrets에 등록합니다.</div>
  </div>);
}

function SelfhostSupabaseStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>Supabase 프로젝트 생성</h2>
    <ol style={S.ol}>
      <li><a href="https://supabase.com/dashboard/projects" target="_blank" rel="noopener" style={S.link}>Supabase Dashboard</a>에서 "New project" 클릭</li>
      <li>프로젝트 이름: <code style={S.code}>wp-auto</code>, 리전: Northeast Asia (ap-northeast-1)</li>
      <li>비밀번호 설정 후 "Create new project"</li>
    </ol>
    <div style={S.box}>
      <strong>SQL 마이그레이션 실행:</strong>
      <ol style={S.ol}>
        <li>좌측 <strong>SQL Editor</strong> 클릭</li>
        <li>Fork한 저장소의 <code style={S.code}>migrations/</code> 폴더에서 SQL 파일 3개를 <strong>순서대로</strong> 복사하여 실행:</li>
      </ol>
      <div style={{ padding: '8px 12px', background: 'var(--input-bg)', borderRadius: 8, fontSize: 12, fontFamily: 'monospace', margin: '8px 0' }}>
        001_consumer_dashboard.sql<br/>
        002_admin_role.sql<br/>
        003_auto_admin_first_user.sql
      </div>
    </div>
    <div style={S.box}>
      <strong>키 메모 (Project Settings &rarr; API):</strong>
      <ul style={S.ul}>
        <li><strong>Project URL</strong> &rarr; SUPABASE_URL</li>
        <li><strong>anon public</strong> key &rarr; NEXT_PUBLIC_SUPABASE_ANON_KEY</li>
        <li><strong>service_role</strong> key &rarr; SUPABASE_SERVICE_KEY</li>
      </ul>
    </div>
    <div style={S.box}>
      <strong>인증 설정 (Authentication &rarr; URL Configuration):</strong>
      <ul style={S.ul}>
        <li>Site URL: <code style={S.code}>https://your-domain.com</code></li>
        <li>Redirect URLs: <code style={S.code}>https://your-domain.com/**</code></li>
      </ul>
    </div>
  </div>);
}

function SelfhostVercelStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>Vercel 배포</h2>
    <ol style={S.ol}>
      <li><a href="https://vercel.com/new" target="_blank" rel="noopener" style={S.link}>Vercel New Project</a>에서 GitHub 연결</li>
      <li>Fork한 <code style={S.code}>wp-auto</code> 저장소 선택</li>
      <li>Environment Variables 5개 입력:</li>
    </ol>
    <table style={S.table}>
      <thead><tr><th style={S.th}>변수명</th><th style={S.th}>값</th></tr></thead>
      <tbody>
        <tr><td style={S.td}><code>NEXT_PUBLIC_SUPABASE_URL</code></td><td style={S.td}>Supabase Project URL</td></tr>
        <tr><td style={S.td}><code>NEXT_PUBLIC_SUPABASE_ANON_KEY</code></td><td style={S.td}>Supabase anon key</td></tr>
        <tr><td style={S.td}><code>SUPABASE_SERVICE_KEY</code></td><td style={S.td}>Supabase service_role key</td></tr>
        <tr><td style={S.td}><code>GITHUB_TOKEN</code></td><td style={S.td}>GitHub PAT (다음 단계에서 생성)</td></tr>
        <tr><td style={S.td}><code>GITHUB_REPO</code></td><td style={S.td}>your-username/wp-auto</td></tr>
      </tbody>
    </table>
    <ol start={4} style={S.ol}>
      <li><strong>Deploy</strong> 클릭</li>
      <li>배포 완료 후 Settings &rarr; Domains에서 커스텀 도메인 연결</li>
    </ol>
    <div style={S.tip}>GitHub Token은 다음 단계에서 생성합니다. 일단 빈 값으로 두고 나중에 추가해도 됩니다.</div>
  </div>);
}

function SelfhostSecretsStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>GitHub Secrets 등록</h2>
    <p>Fork한 저장소에서 <strong>Settings &rarr; Secrets and variables &rarr; Actions</strong>로 이동합니다.</p>
    <a href="https://github.com/settings/tokens/new?scopes=repo,workflow&description=wp-auto" target="_blank" rel="noopener" style={S.bigBtn}>
      GitHub Token 생성하기 &rarr;
    </a>
    <div style={{ fontSize: 11, color: 'var(--text-dim)', marginTop: 4, marginBottom: 16 }}>
      repo + workflow 권한 체크 &rarr; Generate token &rarr; 복사
    </div>
    <div style={S.box}>
      <strong>필수 Secrets (3개):</strong>
      <table style={S.table}>
        <tbody>
          <tr><td style={S.td}><code>SUPABASE_URL</code></td><td style={S.td}>Supabase Project URL</td></tr>
          <tr><td style={S.td}><code>SUPABASE_KEY</code></td><td style={S.td}>Supabase service_role key</td></tr>
          <tr><td style={S.td}><code>DEEPSEEK_API_KEY</code></td><td style={S.td}>DeepSeek API key</td></tr>
        </tbody>
      </table>
    </div>
    <div style={S.box}>
      <strong>선택 Secrets:</strong>
      <table style={S.table}>
        <tbody>
          <tr><td style={S.td}><code>CLAUDE_API_KEY</code></td><td style={S.td}>Claude (폴리싱)</td></tr>
          <tr><td style={S.td}><code>GROK_API_KEY</code></td><td style={S.td}>Grok (보조)</td></tr>
          <tr><td style={S.td}><code>GEMINI_API_KEY</code></td><td style={S.td}>Gemini (보조)</td></tr>
          <tr><td style={S.td}><code>UNSPLASH_ACCESS_KEY</code></td><td style={S.td}>Unsplash (이미지)</td></tr>
          <tr><td style={S.td}><code>PEXELS_API_KEY</code></td><td style={S.td}>Pexels (이미지)</td></tr>
        </tbody>
      </table>
    </div>
    <div style={S.tip}>생성한 GitHub Token은 Vercel 환경변수 GITHUB_TOKEN에도 입력하세요.</div>
  </div>);
}

function SelfhostFirstRunStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>첫 실행</h2>
    <ol style={S.ol}>
      <li>배포된 대시보드 접속 (your-domain.com)</li>
      <li><strong>회원가입</strong> — 첫 가입자가 자동으로 관리자가 됩니다</li>
      <li><strong>설정 &rarr; Step 1</strong>: WordPress URL + 앱 비밀번호 입력 &rarr; "사이트 등록"</li>
      <li><strong>설정 &rarr; Step 2</strong>: 니치 선택 + 기본정보 + 스케줄</li>
      <li><strong>"블로그 시작하기"</strong> 클릭!</li>
    </ol>
    <div style={S.box}>
      <strong>확인 체크리스트:</strong>
      <ul style={S.ul}>
        <li>설정 페이지 하단에 빨간 경고가 없는지 확인</li>
        <li>"블로그 시작하기" 후 5단계 모두 초록색 체크</li>
        <li>WordPress에서 새 글 게시 확인</li>
        <li>GitHub Actions 탭에서 publish.yml 실행 성공 확인</li>
      </ul>
    </div>
  </div>);
}

function SelfhostDailyStep() {
  return (<div style={S.body}>
    <h2 style={S.h2}>일상 운영 + 수익화</h2>
    <div style={S.box}>
      <strong>자동 운영:</strong>
      <ul style={S.ul}>
        <li>GitHub Actions가 하루 4회 (KST 07/12/17/22시) 자동 발행</li>
        <li>대시보드 "홈"에서 발행 현황 확인</li>
        <li>"내 블로그"에서 글 목록 + 품질 점수 확인</li>
      </ul>
    </div>
    <div style={S.box}>
      <strong>수익화 로드맵:</strong>
      <ol style={S.ol}>
        <li><strong>Stage 1</strong> (0~4주): 글 쌓기. 30개+ 도달 후 <a href="https://www.google.com/adsense/start/" target="_blank" rel="noopener" style={S.link}>Google AdSense</a> 신청</li>
        <li><strong>Stage 2</strong> (AdSense 승인 후): 설정에서 Stage 2 전환. <a href="https://partners.coupang.com" target="_blank" rel="noopener" style={S.link}>쿠팡 파트너스</a> + <a href="https://tenping.kr" target="_blank" rel="noopener" style={S.link}>텐핑</a> 등록</li>
        <li><strong>Stage 3</strong> (월 15만+): 전환 키워드 비중 확대. 수익 극대화 모드</li>
      </ol>
    </div>
    <div style={S.tip}>설정 &rarr; "수익화 설정"에서 Stage 전환 + 제휴 링크를 등록하세요.</div>
  </div>);
}

// ── Shared Styles ──

const S = {
  body: { fontSize: 14, lineHeight: 1.8, color: 'var(--text)' },
  h2: { fontSize: 18, fontWeight: 800, marginBottom: 12, color: 'var(--text)' },
  ul: { paddingLeft: 20, margin: '8px 0' },
  ol: { paddingLeft: 20, margin: '8px 0', lineHeight: 2 },
  box: { padding: '14px 16px', background: 'var(--input-bg)', borderRadius: 12, marginBottom: 12, fontSize: 13, lineHeight: 1.8 },
  tip: { padding: '10px 14px', background: 'var(--accent-bg)', borderRadius: 10, fontSize: 12, color: 'var(--accent)', marginTop: 12 },
  warn: { padding: '10px 14px', background: 'var(--red-bg)', borderRadius: 10, fontSize: 12, color: 'var(--red)', marginTop: 12 },
  link: { color: 'var(--accent)', fontWeight: 600, textDecoration: 'underline' },
  code: { padding: '2px 6px', background: 'var(--border-light)', borderRadius: 4, fontSize: 12, fontFamily: 'monospace' },
  bigBtn: {
    display: 'inline-block', padding: '12px 24px', background: 'var(--accent)', color: '#fff',
    borderRadius: 10, fontWeight: 700, fontSize: 14, textDecoration: 'none', marginTop: 8,
  },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: 12, marginTop: 8 },
  th: { textAlign: 'left', padding: '6px 10px', borderBottom: '1px solid var(--border-light)', fontWeight: 700, color: 'var(--text)', fontSize: 11 },
  td: { padding: '6px 10px', borderBottom: '1px solid var(--border-light)' },
};
