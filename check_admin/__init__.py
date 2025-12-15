import azure.functions as func
import json
import sys
import os

# Add parent directory to path for shared_code access
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared_code.database import _get_db_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Check if user is an admin for a specific app.
    Expects JSON: {"ADMIN_EMAIL": "user@example.com", "APP_ID": 123}
    Returns: {"admin": true/false}
    """
    try:
        req_body = req.get_json()
        admin_email = req_body.get('ADMIN_EMAIL')
        app_id = req_body.get('APP_ID')
        
        if not admin_email or not app_id:
            return func.HttpResponse(
                json.dumps({"error": "ADMIN_EMAIL and APP_ID are required"}),
                mimetype="application/json",
                status_code=400
            )
        
        conn = _get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT ADMIN_TYPE FROM APP_ADMINS WHERE ADMIN_EMAIL = ? AND APP_ID = ?"
        cursor.execute(query, (admin_email, app_id))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            admin_type = row[0] if row[0] else None
            result = {
                "admin": True,
                "admin_type": admin_type
            }
        else:
            result = {
                "admin": False,
                "admin_type": None
            }
        
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
