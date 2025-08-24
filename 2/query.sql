SELECT 
    p.name,
    p.age,
    v.visit_date,
    COUNT(s.symptom) as symptom_count
FROM patients p
JOIN visits v ON p.id = v.patient_id
JOIN symptoms s ON v.id = s.visit_id
WHERE p.age > 50 
    AND v.department = 'Neurology'
GROUP BY p.id, v.id
HAVING COUNT(s.symptom) >= 3
ORDER BY v.visit_date DESC
LIMIT 5;