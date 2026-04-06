'use client';
import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

// /onboarding → /settings로 통합 리다이렉트
// addSite 파라미터는 그대로 전달
export default function OnboardingRedirect() {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const addSite = searchParams.get('addSite');
    const target = addSite ? '/settings?addSite=true' : '/settings';
    router.replace(target);
  }, [router, searchParams]);

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '60vh' }}>
      <div style={{ fontSize: 14, color: 'var(--text-dim)' }}>설정 페이지로 이동 중...</div>
    </div>
  );
}
