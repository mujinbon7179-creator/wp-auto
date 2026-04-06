-- dashboard_config 테이블 멀티사이트 지원
-- 기존 global 설정 + 사이트별 개별 설정 병행

-- 1. site_id, config 컬럼 추가
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'dashboard_config' AND column_name = 'site_id') THEN
    ALTER TABLE dashboard_config ADD COLUMN site_id TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'dashboard_config' AND column_name = 'config') THEN
    ALTER TABLE dashboard_config ADD COLUMN config JSONB DEFAULT '{}';
  END IF;
END $$;

-- 2. 기존 global row에 site_id 설정
UPDATE dashboard_config SET site_id = 'global' WHERE id = 'global' AND (site_id IS NULL OR site_id = '');

-- 3. site_id unique index (upsert 지원)
CREATE UNIQUE INDEX IF NOT EXISTS idx_dashboard_config_site_id ON dashboard_config(site_id);

-- 4. bomissu.com 사이트별 설정 삽입
INSERT INTO dashboard_config (id, site_id, config)
VALUES (
  'site-1775046458524',
  'site-1775046458524',
  '{
    "niches": ["beauty", "life-economy", "health-food"],
    "schedule_times": ["08:30", "12:30", "19:30"],
    "daily_count": 3,
    "monetization_stage": 1
  }'::jsonb
)
ON CONFLICT (site_id) DO UPDATE SET config = EXCLUDED.config;

-- 5. planx-ai.com (site-1) 사이트별 설정 삽입
INSERT INTO dashboard_config (id, site_id, config)
VALUES (
  'site-1',
  'site-1',
  '{
    "niches": ["ai-tools", "finance-invest", "side-income"],
    "schedule_times": ["08:00", "20:00"],
    "daily_count": 2,
    "monetization_stage": 1
  }'::jsonb
)
ON CONFLICT (site_id) DO UPDATE SET config = EXCLUDED.config;
