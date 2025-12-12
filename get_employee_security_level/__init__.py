import azure.functions as func
import json
import sys
import os

# Add shared_code to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from shared_code.database import _get_dw_stagin2_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Get security level for a specific employee.
    Expects JSON: {"EMPLOYEE_CODE": "emp_code"}
    Returns: {"TITLE_GROUP_SECURITY_LEVEL": "level_value"}
    """
    try:
        req_body = req.get_json()
        employee_code = req_body.get('EMPLOYEE_CODE')
        
        if not employee_code:
            return func.HttpResponse(
                json.dumps({"error": "EMPLOYEE_CODE is required"}),
                mimetype="application/json",
                status_code=400
            )
        
        conn = _get_dw_stagin2_connection()
        cursor = conn.cursor()
        
        query = "SELECT TITLE_GROUP_SECURITY_LEVEL FROM EMPLOYEE_SECURITY_0 WHERE EMPLOYEE_CODE = ?"
        cursor.execute(query, (employee_code,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            return func.HttpResponse(
                json.dumps({"TITLE_GROUP_SECURITY_LEVEL": row[0]}),
                mimetype="application/json",
                status_code=200
            )
        else:
            return func.HttpResponse(
                json.dumps({"error": "EMPLOYEE_CODE not found"}),
                mimetype="application/json",
                status_code=404
            )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
