SELECT *, salary*12*age as total
FROM `{{ params.AF_TASK_INPUT_TABLE }}` table
WHERE table.timestamp > DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL -1 HOUR)
