# Authorization Service

A simple Flask API for querying SQL Server databases.

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Create a `.env` file with your database credentials:
```
DB_SERVER=your_server_name
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

3. Run the app:
```
python app.py
```

## Usage

Send POST requests to `http://localhost:5000/query` with JSON payload:

```json
{
  "table": "YourTableName",
  "params": {
    "column_name": "value"
  }
}
```

Example response:
```json
{
  "success": true,
  "data": [
    {"id": 1, "name": "John", "email": "john@example.com"}
  ]
}
```
