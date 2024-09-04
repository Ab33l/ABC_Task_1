from flask import Flask, render_template_string
import psycopg2
import pandas as pd

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ABC_Task1",
        user="your_username",
        password="your_password"
    )
    return conn

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

@app.route('/')
def index():
    conn = get_db_connection()
    df1 = pd.read_sql_query(query1, conn)
    df2 = pd.read_sql_query(query2, conn)
    df3 = pd.read_sql_query(query3, conn)
    conn.close()

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
        {{ table1 | safe }}
        <h2>Owners and Their Service History</h2>
        {{ table2 | safe }}
        <h2>Vehicle Models and Service Frequency</h2>
        {{ table3 | safe }}
    </body>
    </html>
    """

    return render_template_string(html_template,
                                  table1=df1.to_html(index=False, classes='table'),
                                  table2=df2.to_html(index=False, classes='table'),
                                  table3=df3.to_html(index=False, classes='table'))

if __name__ == '__main__':
    app.run(debug=True)
