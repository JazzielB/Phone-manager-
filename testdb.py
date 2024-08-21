from sqlalchemy import create_engine
from urllib.parse import quote_plus
# Parámetros de conexión
server = 'SQL8005.site4now.net'
db_name = 'db_a9d1fc_tsiai_admin'
user = 'db_a9d1fc_tsiai_admin'
password = 'TSI555$$$'
dsn = "ODBC Driver 18 for SQL Server"

# Cadena de conexión
engine = create_engine(f"mssql+pyodbc://{user}:%s@{server}/{db_name}?TrustServerCertificate=yes&driver={dsn}" % quote_plus(password))

connection = engine.connect()

print("connected")