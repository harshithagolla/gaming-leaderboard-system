-- schema.sql
CREATE DATABASE IF NOT EXISTS leaderboard_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE leaderboard_db;

-- users
CREATE TABLE IF NOT EXISTS users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- game_sessions
CREATE TABLE IF NOT EXISTS game_sessions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  score INT NOT NULL,
  game_mode VARCHAR(50) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- INDEX for user-based analytics & fast lookups
CREATE INDEX idx_game_sessions_user_id ON game_sessions (user_id);

-- leaderboard (store aggregated total_score only)
CREATE TABLE IF NOT EXISTS leaderboard (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL UNIQUE,
  total_score BIGINT NOT NULL DEFAULT 0,
  INDEX idx_total_score (total_score),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;


-- Unique index ensures atomic UPSERT
ALTER TABLE leaderboard
    ADD UNIQUE INDEX uq_leaderboard_user (user_id);

-- Index to accelerate ORDER BY + rank calculation
CREATE INDEX idx_leaderboard_total_score_desc 
    ON leaderboard (total_score DESC);
