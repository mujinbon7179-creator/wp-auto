'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function SetupGuideRedirect() {
  const router = useRouter();
  useEffect(() => { router.replace('/guide'); }, [router]);
  return <div style={{ padding: 40, textAlign: 'center', color: 'var(--text-dim)' }}>가이드로 이동 중...</div>;
}
