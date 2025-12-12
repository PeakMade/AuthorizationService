import azure.functions as func
import json
import sys
import os

# Add shared_code to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from shared_code.database import _get_db_connection, _get_dw_stagin2_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
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
        req_body = req.get_json()
        admin_email = req_body.get('ADMIN_EMAIL')
        app_id = req_body.get('APP_ID')
        employee_code = req_body.get('EMPLOYEE_CODE')
        
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
        
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
