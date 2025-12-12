import pyodbc
import os

def _get_db_connection():
    """
    Establish connection to main database (DW_APP_SUPPORT).
    Contains APP_ADMINS and APP_LIST tables.
    """
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    
    environment = os.getenv('ENVIRONMENT', 'local').lower()
    driver = 'ODBC Driver 18 for SQL Server' if environment == 'azure' else 'SQL Server'
    
    conn_str = f"DRIVER={{{driver}}};SERVER={server},1433;DATABASE={database};UID={username};PWD={password};Encrypt=no;TrustServerCertificate=yes;"
    conn = pyodbc.connect(conn_str, timeout=10)
    return conn


def _get_dw_stagin2_connection():
    """
    Establish connection to second database (DW_STAGIN2).
    Contains EMPLOYEE_SECURITY_0 table.
    """
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME2')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    
    environment = os.getenv('ENVIRONMENT', 'local').lower()
    driver = 'ODBC Driver 18 for SQL Server' if environment == 'azure' else 'SQL Server'
    
    conn_str = f"DRIVER={{{driver}}};SERVER={server},1433;DATABASE={database};UID={username};PWD={password};Encrypt=no;TrustServerCertificate=yes;"
    conn = pyodbc.connect(conn_str, timeout=10)
    return conn
