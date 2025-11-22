from sqlalchemy import create_engine, text

DB_USER = "postgres"
DB_PASSWORD = "0535"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "caregivers_db"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def create_sql_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        sql_content = file.read()
    
    with engine.begin() as connection:
        connection.execute(text(sql_content))

def execute_and_print(query):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        if result.returns_rows:
            rows = result.fetchall()
            for row in rows:
                print(row)
        connection.commit()


print("1. Create SQL Statements")
create_sql_from_file('database.sql')

print("\n2. Insert SQL Statements")

print("\n3. Update SQL Statement")
update_query_3_1 = """
UPDATE "USER" 
SET phone_number = '+77773414141' 
WHERE given_name = 'Arman' AND surname = 'Armanov';
"""

print("\nQuery 3.1")
execute_and_print(update_query_3_1)

check_3_1 = """
SELECT user_id, given_name, surname, phone_number 
FROM "USER" 
WHERE given_name = 'Arman' AND surname = 'Armanov';
"""
execute_and_print(check_3_1)

update_query_3_2 = """
UPDATE CAREGIVER 
SET hourly_rate = CASE 
    WHEN hourly_rate < 1000.00 THEN hourly_rate + 30.00
    ELSE hourly_rate * 1.10
END;
"""

print("\nQuery 3.2")
execute_and_print(update_query_3_2)

check_3_2 = """
SELECT c.caregiver_user_id, u.given_name || ' ' || u.surname AS caregiver_name, c.hourly_rate
FROM CAREGIVER c
JOIN "USER" u ON c.caregiver_user_id = u.user_id
ORDER BY c.caregiver_user_id;
"""
execute_and_print(check_3_2)


print("\n4. Delete SQL Statement")
delete_query_4_1 = """
DELETE FROM JOB 
WHERE member_user_id = (
    SELECT member_user_id 
    FROM MEMBER 
    WHERE member_user_id = (
        SELECT user_id 
        FROM "USER" 
        WHERE given_name = 'Amina' AND surname = 'Aminova'
    )
);
"""

print("\nQuery 4.1")
execute_and_print(delete_query_4_1)

check_4_1 = """
SELECT j.job_id, j.member_user_id, u.given_name || ' ' || u.surname AS member_name
FROM JOB j
JOIN MEMBER m ON j.member_user_id = m.member_user_id
JOIN "USER" u ON m.member_user_id = u.user_id
ORDER BY j.job_id;
"""
execute_and_print(check_4_1)

delete_query_4_2 = """
DELETE FROM MEMBER 
WHERE member_user_id IN (
    SELECT member_user_id 
    FROM ADDRESS 
    WHERE street = 'Kabanbay Batyr'
);
"""

print("\nQuery 4.2")
execute_and_print(delete_query_4_2)

check_4_2 = """
SELECT m.member_user_id, u.given_name || ' ' || u.surname AS member_name, a.street, a.house_number
FROM MEMBER m
JOIN "USER" u ON m.member_user_id = u.user_id
JOIN ADDRESS a ON m.member_user_id = a.member_user_id
ORDER BY m.member_user_id;
"""
execute_and_print(check_4_2)

print("\n5. Simple Queries")
query_5_1 = """
SELECT 
    cg.given_name || ' ' || cg.surname AS caregiver_name,
    m.given_name || ' ' || m.surname AS member_name
FROM APPOINTMENT a
JOIN "USER" cg ON a.caregiver_user_id = cg.user_id
JOIN "USER" m ON a.member_user_id = m.user_id
WHERE a.status = 'accepted';
"""

print("\nQuery 5.1")
execute_and_print(query_5_1)

query_5_2 = """
SELECT job_id 
FROM JOB 
WHERE other_requirements LIKE '%soft-spoken%';
"""

print("\nQuery 5.2")
execute_and_print(query_5_2)

query_5_3 = """
SELECT a.work_hours 
FROM APPOINTMENT a
JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
WHERE c.caregiving_type = 'babysitter';
"""

print("\nQuery 5.3")
execute_and_print(query_5_3)

query_5_4 = """
SELECT DISTINCT u.given_name, u.surname, u.city
FROM "USER" u
JOIN MEMBER m ON u.user_id = m.member_user_id
JOIN JOB j ON m.member_user_id = j.member_user_id
JOIN ADDRESS a ON m.member_user_id = a.member_user_id
WHERE j.required_caregiving_type = 'elderly_care'
  AND u.city = 'Astana'
  AND m.house_rules LIKE '%No pets%';
"""

print("\nQuery 5.4")
execute_and_print(query_5_4)


print("\n6. Complex Queries")
query_6_1 = """
SELECT 
    j.job_id,
    u.given_name || ' ' || u.surname AS member_name,
    COUNT(ja.caregiver_user_id) AS number_of_applicants
FROM JOB j
JOIN MEMBER m ON j.member_user_id = m.member_user_id
JOIN "USER" u ON m.member_user_id = u.user_id
LEFT JOIN JOB_APPLICATION ja ON j.job_id = ja.job_id
GROUP BY j.job_id, u.given_name, u.surname
ORDER BY j.job_id;
"""

print("\nQuery 6.1")
execute_and_print(query_6_1)

query_6_2 = """
SELECT 
    SUM(a.work_hours) AS total_hours
FROM APPOINTMENT a
WHERE a.status = 'accepted';
"""

print("\nQuery 6.2")
execute_and_print(query_6_2)

query_6_3 = """
SELECT 
    AVG(c.hourly_rate) AS average_hourly_rate
FROM APPOINTMENT a
JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
WHERE a.status = 'accepted';
"""

print("\nQuery 6.3")
execute_and_print(query_6_3)

query_6_4 = """
SELECT 
    u.given_name || ' ' || u.surname AS caregiver_name,
    c.hourly_rate
FROM CAREGIVER c
JOIN "USER" u ON c.caregiver_user_id = u.user_id
JOIN APPOINTMENT a ON c.caregiver_user_id = a.caregiver_user_id
WHERE a.status = 'accepted'
  AND c.hourly_rate > (
      SELECT AVG(c2.hourly_rate)
      FROM CAREGIVER c2
      JOIN APPOINTMENT a2 ON c2.caregiver_user_id = a2.caregiver_user_id
      WHERE a2.status = 'accepted'
  )
GROUP BY u.given_name, u.surname, c.hourly_rate;
"""

print("\nQuery 6.4")
execute_and_print(query_6_4)


print("\n7. Query with a Derived Attribute")
query_7 = """
SELECT 
    a.appointment_id,
    u.given_name || ' ' || u.surname AS caregiver_name,
    c.hourly_rate,
    a.work_hours,
    (c.hourly_rate * a.work_hours) AS total_cost
FROM APPOINTMENT a
JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
JOIN "USER" u ON c.caregiver_user_id = u.user_id
WHERE a.status = 'accepted'
ORDER BY a.appointment_id;
"""

print("\nQuery 7")
execute_and_print(query_7)


print("\n8. View Operation ")
query_8_create = """
CREATE OR REPLACE VIEW job_applications_view AS
SELECT 
    ja.job_id,
    j.required_caregiving_type,
    ja.date_applied,
    u_cg.user_id AS applicant_id,
    u_cg.given_name || ' ' || u_cg.surname AS applicant_name,
    c.caregiving_type AS applicant_caregiving_type,
    c.hourly_rate,
    u_mem.user_id AS job_poster_id,
    u_mem.given_name || ' ' || u_mem.surname AS job_poster_name
FROM JOB_APPLICATION ja
JOIN JOB j ON ja.job_id = j.job_id
JOIN CAREGIVER c ON ja.caregiver_user_id = c.caregiver_user_id
JOIN "USER" u_cg ON c.caregiver_user_id = u_cg.user_id
JOIN MEMBER m ON j.member_user_id = m.member_user_id
JOIN "USER" u_mem ON m.member_user_id = u_mem.user_id;
"""
execute_and_print(query_8_create)
print("\nQuery 8 -> View is created")
query_8 = "SELECT * FROM job_applications_view ORDER BY job_id, date_applied;"

print("\nQuery 8")
execute_and_print(query_8)

print("\nPart 2 completed")
print("\nDatabase connection closed.")
engine.dispose()
