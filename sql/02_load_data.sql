-- Food Waste Management System — Data Load Instructions
-- Load CSV files from the raw/ directory after schema creation.
--
-- PostgreSQL example (run from project root):
--   \copy providers FROM 'raw/providers_data.csv' WITH (FORMAT csv, HEADER true);
--   \copy receivers FROM 'raw/receivers_data.csv' WITH (FORMAT csv, HEADER true);
--   \copy food_listings FROM 'raw/food_listings_data.csv' WITH (FORMAT csv, HEADER true);
--   \copy claims FROM 'raw/claims_data.csv' WITH (FORMAT csv, HEADER true);
--
-- SQLite example:
--   .mode csv
--   .import raw/providers_data.csv providers
--   .import raw/receivers_data.csv receivers
--   .import raw/food_listings_data.csv food_listings
--   .import raw/claims_data.csv claims
-- Post-load validation queries
SELECT
  'providers' AS table_name,
  COUNT(*) AS row_count
FROM
  providers
UNION ALL
SELECT
  'receivers',
  COUNT(*)
FROM
  receivers
UNION ALL
SELECT
  'food_listings',
  COUNT(*)
FROM
  food_listings
UNION ALL
SELECT
  'claims',
  COUNT(*)
FROM
  claims;

-- Referential integrity checks (should return 0 rows each)
SELECT
  c.claim_id,
  c.food_id
FROM
  claims c
  LEFT JOIN food_listings f ON c.food_id = f.food_id
WHERE
  f.food_id IS NULL;

SELECT
  c.claim_id,
  c.receiver_id
FROM
  claims c
  LEFT JOIN receivers r ON c.receiver_id = r.receiver_id
WHERE
  r.receiver_id IS NULL;

SELECT
  f.food_id,
  f.provider_id
FROM
  food_listings f
  LEFT JOIN providers p ON f.provider_id = p.provider_id
WHERE
  p.provider_id IS NULL;