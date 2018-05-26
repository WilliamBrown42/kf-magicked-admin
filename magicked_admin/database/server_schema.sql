CREATE TABLE player(
    steam_id CHAR(17) PRIMARY KEY, -- Unique 17 Char steam id
    username VARCHAR(32), -- Steam permits up to 32 characters in username
    country_code CHAR(2) -- ISO ALPHA-2 Code
);

CREATE TABLE game(
    game_id INTEGER PRIMARY KEY,
    map_id INTEGER,
    game_mode VARCHAR(64),
    difficulty VARCHAR(64),
    game_length INTEGER,
    date_start VARCHAR(32) NOT NULL,
    date_end VARCHAR(32)
);

CREATE TABLE game_session(
    game_id INTEGER PRIMARY KEY,
    session_id INTEGER
);

CREATE TABLE session(
    session_id INTEGER PRIMARY KEY,
    steam_id VARCHAR(16),
    kills INTEGER DEFAULT 0,
    deaths INTEGER DEFAULT 0,
    dosh_earned INTEGER DEFAULT 0,
    dosh_spent INTEGER DEFAULT 0,
    date_start VARCHAR(32) NOT NULL,
    date_end VARCHAR(32)
);

<<<<<<< HEAD
CREATE TABLE map(
    map_id INTEGER PRIMARY KEY,
    title VARCHAR(64) UNIQUE,
CREATE TABLE maps(
    name VARCHAR(64) PRIMARY KEY,
    title VARCHAR(64) DEFAULT "Unnamed",
    plays_survival INTEGER DEFAULT 0,
    plays_weekly INTEGER DEFAULT 0,
    plays_endless INTEGER DEFAULT 0,
    plays_survival_vs INTEGER DEFAULT 0,
    plays_other INTEGER DEFAULT 0,
    highest_wave INTEGER DEFAULT 0
>>>>>>> master
);
