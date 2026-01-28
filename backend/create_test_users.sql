-- Script SQL pour créer les comptes de test
-- Exécuter avec: sqlite3 strategic.db < create_test_users.sql

-- Note: Les mots de passe sont hashés avec bcrypt
-- Mot de passe pour tous: Test2026!

-- 1. Admin
INSERT OR IGNORE INTO users (email, hashed_password, full_name, is_superuser, is_active)
VALUES ('admin@strategic.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfj3NnqyNG', 'Strategic Admin', 1, 1);

-- 2. Fondateur
INSERT OR IGNORE INTO users (email, hashed_password, full_name, is_superuser, is_active)
VALUES ('fondateur@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfj3NnqyNG', 'User Fondateur', 0, 1);

-- 3. Stratège
INSERT OR IGNORE INTO users (email, hashed_password, full_name, is_superuser, is_active)
VALUES ('stratege@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfj3NnqyNG', 'User Stratège', 0, 1);

-- 4. Visionnaire
INSERT OR IGNORE INTO users (email, hashed_password, full_name, is_superuser, is_active)
VALUES ('visionnaire@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfj3NnqyNG', 'User Visionnaire', 0, 1);

-- Créer les abonnements
INSERT OR IGNORE INTO subscriptions (user_id, plan, reports_limit, is_active)
SELECT id, 'visionary', 9999, 1 FROM users WHERE email = 'admin@strategic.com';

INSERT OR IGNORE INTO subscriptions (user_id, plan, reports_limit, is_active)
SELECT id, 'founder', 3, 1 FROM users WHERE email = 'fondateur@test.com';

INSERT OR IGNORE INTO subscriptions (user_id, plan, reports_limit, is_active)
SELECT id, 'strategist', 10, 1 FROM users WHERE email = 'stratege@test.com';

INSERT OR IGNORE INTO subscriptions (user_id, plan, reports_limit, is_active)
SELECT id, 'visionary', 9999, 1 FROM users WHERE email = 'visionnaire@test.com';
