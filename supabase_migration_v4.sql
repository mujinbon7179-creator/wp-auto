-- ============================================================
-- AutoBlog Dashboard v4.0 Migration
-- publish_logs에 quality_score 추가
-- Supabase Dashboard → SQL Editor → 실행
-- ============================================================

ALTER TABLE publish_logs ADD COLUMN IF NOT EXISTS quality_score INT DEFAULT 0;

CREATE INDEX IF NOT EXISTS idx_publish_quality ON publish_logs(quality_score DESC);
