-- 创建 actors 数据库（若不存在）
CREATE DATABASE IF NOT EXISTS actors;
-- 使用 actors 数据库
USE actors;

-- 创建 characters 表（若不存在）
CREATE TABLE IF NOT EXISTS characters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    health INT NOT NULL,
    attack INT NOT NULL,
    defense INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 开启事务保证数据完整性
START TRANSACTION;
-- 清空 characters 表现有数据
DELETE FROM characters;
-- 重置自增 ID 为 1
ALTER TABLE characters AUTO_INCREMENT = 1;

-- 向 characters 表插入数据
INSERT INTO characters (name, health, attack, defense) VALUES 
('钟离', 13000, 2000, 800),
('甘雨', 10000, 2200, 700),
('雷电将军', 11000, 2100, 750),
('温迪', 9000, 2300, 650),
('迪卢克', 12000, 2400, 780),
('琴', 10500, 2150, 720),
('刻晴', 9500, 2250, 680),
('七七', 8500, 1800, 700),
('魈', 11500, 2500, 730),
('香菱', 9800, 2050, 690);

-- 若所有操作成功则提交事务
COMMIT;