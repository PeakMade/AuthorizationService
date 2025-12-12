import azure.functions as func
import json
import sys
import os

# Add shared_code to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from shared_code.database import _get_db_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Get security level for a specific app.
    Expects JSON: {"APP_ID": 123}
    Returns: {"App_Security_level": "level_value"}
    """
    try:
        req_body = req.get_json()
        app_id = req_body.get('APP_ID')
        
        if not app_id:
            return func.HttpResponse(
                json.dumps({"error": "APP_ID is required"}),
                mimetype="application/json",
                status_code=400
            )
        
        conn = _get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT App_Security_level FROM APP_LIST WHERE APP_ID = ?"
        cursor.execute(query, (app_id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            return func.HttpResponse(
                json.dumps({"App_Security_level": row[0]}),
                mimetype="application/json",
                status_code=200
            )
        else:
            return func.HttpResponse(
                json.dumps({"error": "APP_ID not found"}),
                mimetype="application/json",
                status_code=404
            )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
