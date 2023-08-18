-- Number of employees with employment status, gender count, and average age
SELECT EmploymentStatus,
       SUM(CASE WHEN GenderID = 0 THEN TerminationCount ELSE 0 END) AS Female,
       SUM(CASE WHEN GenderID = 1 THEN TerminationCount ELSE 0 END) AS Male,
       ROUND(AVG(Age),1) AS AvgAge
FROM (
    SELECT EmploymentStatus,
		   GenderID,
           COUNT(Termd) AS TerminationCount,
           AVG(TIMESTAMPDIFF(YEAR, STR_TO_DATE(DOB, '%m/%d/%Y'), CURDATE())) AS Age
    FROM hrdataset
    GROUP BY EmploymentStatus, GenderID
) AS TerminationSummary
GROUP BY EmploymentStatus;

-- Absence rate (assume 260 working days), Punctuality Index 
SELECT EmploymentStatus, ROUND(AVG(Absences/260)*100, 2) AS Absence_rate, ROUND(AVG(DaysLateLast30), 2) AS DaysLateLast30
FROM hrdataset
GROUP BY EmploymentStatus;

-- Absence rate (assume 260 working days), Punctuality Index, Group by department for current employee
SELECT Department, ROUND(AVG(Absences/260)*100, 2) AS Absence_rate, ROUND(AVG(DaysLateLast30), 2) AS Days_Late_Last_30
FROM hrdataset
WHERE Termd = 0
GROUP BY Department
ORDER BY Absence_rate DESC;

-- Emoloyee Satisfaction. Dissatisfaction is a common cause of employee turnover.
SELECT Department, ROUND(AVG(EmpSatisfaction), 2) AS Emoloyee_Satisfaction
FROM hrdataset
WHERE Termd = 0
GROUP BY Department
ORDER BY Emoloyee_Satisfaction DESC;

-- Employee engagement. 
SELECT Department, ROUND(AVG(EngagementSurvey), 2) AS Emoloyee_Engagement
FROM hrdataset
WHERE Termd = 0
GROUP BY Department
ORDER BY Emoloyee_Engagement DESC;

-- 360-day quit rate and create VIEW
CREATE VIEW QuitMetricsView AS
WITH QuitData AS (SELECT DATEDIFF(STR_TO_DATE(DateofTermination, '%m/%d/%Y'), STR_TO_DATE(DateofHire, '%m/%d/%Y')) AS DaysBetween
    FROM hrdataset
    WHERE Termd = 1
)
SELECT (SELECT COUNT(*) FROM QuitData) AS TotalQuits,
	   COUNT(*) AS 360_day_QuitCount, 
	   ROUND(COUNT(*) / (SELECT COUNT(*) FROM QuitData)*100, 2) AS 360_day_QuitRate
FROM QuitData
WHERE DaysBetween <= 360;

SELECT * FROM QuitMetricsView;

-- Average Employee Tenure
SELECT ROUND(AVG(DaysBetween)/365, 2) AS AverageTenure
FROM (SELECT CASE WHEN Termd = 1 THEN DATEDIFF(STR_TO_DATE(DateofTermination, '%m/%d/%Y'), STR_TO_DATE(DateofHire, '%m/%d/%Y'))
		          ELSE DATEDIFF(CURDATE(), STR_TO_DATE(DateofHire, '%m/%d/%Y'))
                  END AS DaysBetween
FROM hrdataset) AS TenureData;

-- Performance Table
SELECT Department, 
	   SUM(CASE WHEN PerfScoreID = 1 THEN 1 ELSE 0 END) AS "1", 
       SUM(CASE WHEN PerfScoreID = 2 THEN 1 ELSE 0 END) AS "2", 
       SUM(CASE WHEN PerfScoreID = 3 THEN 1 ELSE 0 END) AS "3", 
       SUM(CASE WHEN PerfScoreID = 4 THEN 1 ELSE 0 END) AS "4",
       ROUND(AVG(PerfScoreID), 2) AS AvgScore
FROM hrdataset
WHERE Termd = 0
GROUP BY Department
ORDER BY AvgScore, Department;
