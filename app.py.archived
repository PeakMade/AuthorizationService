from flask import Flask, request, jsonify
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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


@app.route('/check_admin', methods=['POST'])
def check_admin():
    """
    Check if user is an admin for a specific app.
    Expects JSON: {"ADMIN_EMAIL": "user@example.com", "APP_ID": 123}
    Returns: {"admin": true/false}
    """
    try:
        data = request.get_json()
        admin_email = data.get('ADMIN_EMAIL')
        app_id = data.get('APP_ID')
        
        if not admin_email or not app_id:
            return jsonify({"error": "ADMIN_EMAIL and APP_ID are required"}), 400
        
        conn = _get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) FROM APP_ADMINS WHERE ADMIN_EMAIL = ? AND APP_ID = ?"
        cursor.execute(query, (admin_email, app_id))
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return jsonify({"admin": count > 0}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_app_security_level', methods=['POST'])
def get_app_security_level():
    """
    Get security level for a specific app.
    Expects JSON: {"APP_ID": 123}
    Returns: {"App_Security_level": "level_value"}
    """
    try:
        data = request.get_json()
        app_id = data.get('APP_ID')
        
        if not app_id:
            return jsonify({"error": "APP_ID is required"}), 400
        
        conn = _get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT App_Security_level FROM APP_LIST WHERE APP_ID = ?"
        cursor.execute(query, (app_id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            return jsonify({"App_Security_level": row[0]}), 200
        else:
            return jsonify({"error": "APP_ID not found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_employee_security_level', methods=['POST'])
def get_employee_security_level():
    """
    Get security level for a specific employee.
    Expects JSON: {"EMPLOYEE_CODE": "emp_code"}
    Returns: {"TITLE_GROUP_SECURITY_LEVEL": "level_value"}
    """
    try:
        data = request.get_json()
        employee_code = data.get('EMPLOYEE_CODE')
        
        if not employee_code:
            return jsonify({"error": "EMPLOYEE_CODE is required"}), 400
        
        conn = _get_dw_stagin2_connection()
        cursor = conn.cursor()
        
        query = "SELECT TITLE_GROUP_SECURITY_LEVEL FROM EMPLOYEE_SECURITY_0 WHERE EMPLOYEE_CODE = ?"
        cursor.execute(query, (employee_code,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            return jsonify({"TITLE_GROUP_SECURITY_LEVEL": row[0]}), 200
        else:
            return jsonify({"error": "EMPLOYEE_CODE not found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_authorization', methods=['POST'])
def get_authorization():
    """
    Get all authorization info in one request.
    Expects JSON: {"ADMIN_EMAIL": "user@example.com", "APP_ID": 123, "EMPLOYEE_CODE": "emp_code"}
    Returns: {
        "admin": true/false,
        "App_Security_level": "level_value",
        "TITLE_GROUP_SECURITY_LEVEL": "level_value"
    }
    """
    try:
        data = request.get_json()
        admin_email = data.get('ADMIN_EMAIL')
        app_id = data.get('APP_ID')
        employee_code = data.get('EMPLOYEE_CODE')
        
        result = {}
        
        # Check admin status
        if admin_email and app_id:
            conn = _get_db_connection()
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM APP_ADMINS WHERE ADMIN_EMAIL = ? AND APP_ID = ?"
            cursor.execute(query, (admin_email, app_id))
            count = cursor.fetchone()[0]
            result['admin'] = count > 0
            cursor.close()
            conn.close()
        
        # Get app security level
        if app_id:
            conn = _get_db_connection()
            cursor = conn.cursor()
            query = "SELECT App_Security_level FROM APP_LIST WHERE APP_ID = ?"
            cursor.execute(query, (app_id,))
            row = cursor.fetchone()
            result['App_Security_level'] = row[0] if row else None
            cursor.close()
            conn.close()
        
        # Get employee security level
        if employee_code:
            conn = _get_dw_stagin2_connection()
            cursor = conn.cursor()
            query = "SELECT TITLE_GROUP_SECURITY_LEVEL FROM EMPLOYEE_SECURITY_0 WHERE EMPLOYEE_CODE = ?"
            cursor.execute(query, (employee_code,))
            row = cursor.fetchone()
            result['TITLE_GROUP_SECURITY_LEVEL'] = row[0] if row else None
            cursor.close()
            conn.close()
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
