-- ============================================================
-- AutoBlog v6.0 Migration — 멀티사이트 지원
-- sites.config에 사이트별 WP 인증정보 저장
-- Supabase Dashboard → SQL Editor → 실행
-- ============================================================

-- config JSONB에 wp_username, wp_app_password 저장 가능하도록 안내
-- (이미 config JSONB 컬럼 존재하므로 스키마 변경 불필요)

-- 기존 site-1의 config 업데이트 예시:
-- UPDATE sites SET config = jsonb_set(
--   COALESCE(config, '{}'::jsonb),
--   '{wp_username}',
--   '"your_wp_username"'
-- ) WHERE id = 'site-1';

-- 주의: 프로덕션 환경에서는 RLS를 서비스 롤 키로 제한하세요.
-- 현재 anon 키로 전체 접근 허용 상태 (개발용)

SELECT 'Migration v5: 멀티사이트 — 스키마 변경 불필요, sites.config JSONB 활용' AS status;
