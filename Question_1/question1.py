import psycopg2
import pandas as pd
from jinja2 import Template

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="ABC_Task1",
    user="postgres",
    password="JustinFields1$"
)

# SQL Queries
query1 = """
SELECT 
    s.service_date, 
    v.car_model, 
    v.car_registration_number, 
    o.owner_fname AS owner_name, 
    s.cost
FROM 
    services s
JOIN 
    vehicles v ON s.vehicle_id = v.vehicle_id
JOIN 
    owners o ON v.owner_id = o.owner_id
ORDER BY 
    s.service_date;
"""

query2 = """
SELECT 
    o.owner_fname AS owner_name, 
    COUNT(s.service_id) AS service_count, 
    SUM(s.cost) AS total_spent
FROM 
    owners o
JOIN 
    vehicles v ON o.owner_id = v.owner_id
JOIN 
    services s ON v.vehicle_id = s.vehicle_id
GROUP BY 
    o.owner_fname
ORDER BY 
    total_spent DESC;
"""

query3 = """
SELECT 
    v.car_model, 
    COUNT(s.service_id) AS service_frequency, 
    SUM(s.cost) AS total_income
FROM 
    vehicles v
JOIN 
    services s ON v.vehicle_id = s.vehicle_id
GROUP BY 
    v.car_model
ORDER BY 
    service_frequency DESC;
"""

# Execute queries and fetch data
df1 = pd.read_sql_query(query1, conn)
df2 = pd.read_sql_query(query2, conn)
df3 = pd.read_sql_query(query3, conn)

# Close the connection
conn.close()

# HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Service Station Report</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h2>Service Activities</h2>
    {{ table1 }}
    <h2>Owners and Their Service History</h2>
    {{ table2 }}
    <h2>Vehicle Models and Service Frequency</h2>
    {{ table3 }}
</body>
</html>
"""

# Render HTML
template = Template(html_template)
html_content = template.render(
    table1=df1.to_html(index=False, classes='table'),
    table2=df2.to_html(index=False, classes='table'),
    table3=df3.to_html(index=False, classes='table')
)

# Write to HTML file
with open("finalReport.html", "w") as file:
    file.write(html_content)

print("Final Report generated successfully!")
