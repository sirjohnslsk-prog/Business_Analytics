-- Zambia Higher-Education Market Intelligence
-- Portable SQL illustrating the analytical model used by the portfolio project.

CREATE TABLE province_market (
    province VARCHAR(40) PRIMARY KEY,
    population_2022 INTEGER NOT NULL,
    population_2010 INTEGER NOT NULL,
    employment_to_population_2023_pct DECIMAL(5,2),
    poverty_gap_2022_pct DECIMAL(5,2),
    line_of_rail_competition VARCHAR(10),
    public_universities_2023 INTEGER
);

CREATE TABLE programme_fee (
    code VARCHAR(20) PRIMARY KEY,
    programme VARCHAR(160),
    level VARCHAR(30),
    school VARCHAR(100),
    duration VARCHAR(40),
    day_zmw DECIMAL(12,2),
    evening_zmw DECIMAL(12,2),
    weekend_zmw DECIMAL(12,2),
    distance_zmw DECIMAL(12,2)
);

-- Core market view
CREATE VIEW v_province_market AS
SELECT
    province,
    population_2022,
    population_2010,
    ROUND((population_2022 * 1.0 / population_2010 - 1) * 100, 2) AS growth_2010_2022_pct,
    employment_to_population_2023_pct,
    poverty_gap_2022_pct,
    line_of_rail_competition,
    public_universities_2023
FROM province_market;

-- Recruitment-screening query: large market + stronger employment base + lower affordability pressure
SELECT
    province,
    population_2022,
    employment_to_population_2023_pct,
    poverty_gap_2022_pct,
    line_of_rail_competition
FROM v_province_market
ORDER BY population_2022 DESC, employment_to_population_2023_pct DESC;

-- Markets where population grew >50% but competition context is lower.
SELECT province, growth_2010_2022_pct, population_2022
FROM v_province_market
WHERE growth_2010_2022_pct > 50
  AND line_of_rail_competition = 'Lower'
ORDER BY growth_2010_2022_pct DESC;

-- Programme price-band view, deliberately not assuming annual fee frequency.
SELECT
    code,
    programme,
    level,
    COALESCE(day_zmw, evening_zmw, weekend_zmw, distance_zmw) AS first_published_local_fee_zmw
FROM programme_fee
ORDER BY first_published_local_fee_zmw, code;
