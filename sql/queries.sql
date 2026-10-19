-- 1. Список всех лекарств (SELECT + ORDER BY).
SELECT id, name, dosage, unit FROM medicines ORDER BY name;

-- 2. Список пользователей по возрасту.
SELECT id, name, age FROM users ORDER BY age, name;

-- 3. Поиск лекарств по части названия (передавать шаблон параметром).
SELECT id, name, dosage, unit FROM medicines WHERE name LIKE ? ORDER BY name;

-- 4. Фильтрация лекарств по минимальной дозировке.
SELECT id, name, dosage, unit FROM medicines WHERE dosage >= ? ORDER BY dosage;

-- 5. Расписания конкретного пользователя (WHERE).
SELECT id, user_id, medicine_id, hour, minute FROM schedules WHERE user_id = ? ORDER BY hour, minute;

-- 6. История приёмов за выбранную дату.
SELECT id, schedule_id, intake_date, taken FROM intakes WHERE intake_date = ? ORDER BY id;

-- 7. Расписание с лекарством и пользователем (JOIN).
SELECT s.id, u.name AS user_name, m.name AS medicine_name, m.dosage, m.unit,
       s.hour, s.minute
FROM schedules AS s
JOIN users AS u ON u.id = s.user_id
JOIN medicines AS m ON m.id = s.medicine_id
ORDER BY s.hour, s.minute;

-- 8. Подробная история приёмов (JOIN нескольких таблиц).
SELECT i.id, i.intake_date, i.taken, s.hour, s.minute,
       u.name AS user_name, m.name AS medicine_name
FROM intakes AS i
JOIN schedules AS s ON s.id = i.schedule_id
JOIN users AS u ON u.id = s.user_id
JOIN medicines AS m ON m.id = s.medicine_id
ORDER BY i.intake_date DESC, i.id DESC;

-- 9. Общее количество записей о приёмах (COUNT).
SELECT COUNT(*) AS intakes_count FROM intakes;

-- 10. Средняя и максимальная дозировка лекарств (AVG, MAX).
SELECT AVG(dosage) AS average_dosage, MAX(dosage) AS maximum_dosage FROM medicines;

-- 11. Количество расписаний по лекарствам (GROUP BY, включая нулевые значения).
SELECT m.id, m.name AS medicine_name, COUNT(s.id) AS schedules_count
FROM medicines AS m
LEFT JOIN schedules AS s ON s.medicine_id = m.id
GROUP BY m.id, m.name
ORDER BY schedules_count DESC, m.name;

-- 12. Количество приёмов по статусу (GROUP BY).
SELECT taken, COUNT(*) AS records_count
FROM intakes
GROUP BY taken
ORDER BY taken DESC;

-- 13. Лекарства, назначенные более чем в одном расписании (HAVING).
SELECT m.id, m.name, COUNT(s.id) AS schedules_count
FROM medicines AS m
JOIN schedules AS s ON s.medicine_id = m.id
GROUP BY m.id, m.name
HAVING COUNT(s.id) > ?
ORDER BY schedules_count DESC;
