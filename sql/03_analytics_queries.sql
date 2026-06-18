-- Food Waste Management System — Executive Analytics Queries

-- ── KPI Summary ──────────────────────────────────────────────────────────────
SELECT
    (SELECT SUM(quantity) FROM food_listings)                                          AS total_food_units,
    (SELECT COUNT(*) FROM claims)                                                      AS total_claims,
    (SELECT COUNT(*) FROM claims WHERE status = 'Completed')                           AS completed_claims,
    ROUND(100.0 * (SELECT COUNT(*) FROM claims WHERE status = 'Completed')
          / NULLIF((SELECT COUNT(*) FROM claims), 0), 1)                               AS claim_success_pct,
    ROUND(100.0 * (SELECT SUM(f.quantity)
                   FROM food_listings f
                   JOIN claims c ON f.food_id = c.food_id
                   WHERE c.status = 'Completed')
          / NULLIF((SELECT SUM(quantity) FROM food_listings), 0), 1)                   AS food_rescue_pct;

-- ── Claim Status Distribution ────────────────────────────────────────────────
SELECT status, COUNT(*) AS claim_count,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM claims
GROUP BY status
ORDER BY claim_count DESC;

-- ── Food Supply by Type ──────────────────────────────────────────────────────
SELECT food_type, SUM(quantity) AS total_quantity,
       ROUND(100.0 * SUM(quantity) / SUM(SUM(quantity)) OVER (), 1) AS pct
FROM food_listings
GROUP BY food_type
ORDER BY total_quantity DESC;

-- ── Provider Contribution ────────────────────────────────────────────────────
SELECT p.type AS provider_type,
       COUNT(DISTINCT p.provider_id) AS provider_count,
       SUM(f.quantity) AS total_donated
FROM providers p
JOIN food_listings f ON p.provider_id = f.provider_id
GROUP BY p.type
ORDER BY total_donated DESC;

-- ── Top 10 Providers by Donation Volume ──────────────────────────────────────
SELECT p.name, p.type, p.city, SUM(f.quantity) AS total_donated
FROM providers p
JOIN food_listings f ON p.provider_id = f.provider_id
GROUP BY p.provider_id, p.name, p.type, p.city
ORDER BY total_donated DESC
LIMIT 10;

-- ── Receiver Demand by Type ──────────────────────────────────────────────────
SELECT r.type AS receiver_type, COUNT(c.claim_id) AS total_claims,
       SUM(CASE WHEN c.status = 'Completed' THEN 1 ELSE 0 END) AS completed
FROM receivers r
JOIN claims c ON r.receiver_id = c.receiver_id
GROUP BY r.type
ORDER BY total_claims DESC;

-- ── Geographic Supply vs Demand (Top 15 Cities) ──────────────────────────────
WITH supply AS (
    SELECT location AS city, SUM(quantity) AS supply_units
    FROM food_listings
    GROUP BY location
),
demand AS (
    SELECT f.location AS city, COUNT(c.claim_id) AS claim_count
    FROM claims c
    JOIN food_listings f ON c.food_id = f.food_id
    GROUP BY f.location
)
SELECT s.city, s.supply_units, COALESCE(d.claim_count, 0) AS claim_count
FROM supply s
LEFT JOIN demand d ON s.city = d.city
ORDER BY s.supply_units DESC
LIMIT 15;

-- ── Cancellation Analysis by Provider Type ───────────────────────────────────
SELECT f.provider_type, COUNT(*) AS cancellations
FROM claims c
JOIN food_listings f ON c.food_id = f.food_id
WHERE c.status = 'Cancelled'
GROUP BY f.provider_type
ORDER BY cancellations DESC;

-- ── Enriched Claims View ─────────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_claims_enriched AS
SELECT
    c.claim_id,
    c.status,
    c.timestamp,
    f.food_id,
    f.food_name,
    f.quantity,
    f.food_type,
    f.meal_type,
    f.location,
    f.provider_type,
    p.name   AS provider_name,
    p.city   AS provider_city,
    r.name   AS receiver_name,
    r.type   AS receiver_type,
    r.city   AS receiver_city
FROM claims c
LEFT JOIN food_listings f ON c.food_id = f.food_id
LEFT JOIN providers p     ON f.provider_id = p.provider_id
LEFT JOIN receivers r     ON c.receiver_id = r.receiver_id;
