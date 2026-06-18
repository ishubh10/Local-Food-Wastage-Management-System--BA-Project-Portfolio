-- Food Waste Management System — DDL
-- Compatible with PostgreSQL / SQLite (minor type adjustments may apply)

DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS food_listings;
DROP TABLE IF EXISTS receivers;
DROP TABLE IF EXISTS providers;

CREATE TABLE providers (
    provider_id   INTEGER PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    type            VARCHAR(50)  NOT NULL
                    CHECK (type IN ('Supermarket', 'Grocery Store', 'Restaurant', 'Catering Service')),
    address         TEXT         NOT NULL,
    city            VARCHAR(100) NOT NULL,
    contact         VARCHAR(50)  NOT NULL
);

CREATE TABLE receivers (
    receiver_id   INTEGER PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    type            VARCHAR(50)  NOT NULL
                    CHECK (type IN ('NGO', 'Charity', 'Shelter', 'Individual')),
    city            VARCHAR(100) NOT NULL,
    contact         VARCHAR(50)  NOT NULL
);

CREATE TABLE food_listings (
    food_id         INTEGER PRIMARY KEY,
    food_name       VARCHAR(100) NOT NULL,
    quantity        INTEGER      NOT NULL CHECK (quantity > 0),
    expiry_date     DATE         NOT NULL,
    provider_id     INTEGER      NOT NULL REFERENCES providers(provider_id),
    provider_type   VARCHAR(50)  NOT NULL,
    location        VARCHAR(100) NOT NULL,
    food_type       VARCHAR(50)  NOT NULL
                    CHECK (food_type IN ('Vegan', 'Vegetarian', 'Non-Vegetarian')),
    meal_type       VARCHAR(50)  NOT NULL
                    CHECK (meal_type IN ('Breakfast', 'Lunch', 'Dinner', 'Snacks'))
);

CREATE TABLE claims (
    claim_id      INTEGER PRIMARY KEY,
    food_id         INTEGER      NOT NULL REFERENCES food_listings(food_id),
    receiver_id     INTEGER      NOT NULL REFERENCES receivers(receiver_id),
    status          VARCHAR(20)  NOT NULL
                    CHECK (status IN ('Completed', 'Pending', 'Cancelled')),
    timestamp       TIMESTAMP    NOT NULL
);

CREATE INDEX idx_claims_status      ON claims(status);
CREATE INDEX idx_claims_timestamp   ON claims(timestamp);
CREATE INDEX idx_claims_food_id     ON claims(food_id);
CREATE INDEX idx_claims_receiver_id ON claims(receiver_id);
CREATE INDEX idx_food_provider_id   ON food_listings(provider_id);
CREATE INDEX idx_food_location      ON food_listings(location);
CREATE INDEX idx_food_type          ON food_listings(food_type);
