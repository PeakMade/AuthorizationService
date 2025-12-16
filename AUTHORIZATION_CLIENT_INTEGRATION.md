# Authorization Service - Client Integration Guide

## Overview
This service provides authorization and security level information for applications. To optimize performance, **cache authorization results in the user's session** to avoid repeated API calls.

---

## Setup Requirements

**Before implementing:**
1. **Store your APP_ID as an environment variable** in your application (e.g., `APP_ID=123`)
2. **Obtain the employee code and email from your authentication system** - Your app should receive these values during user login/authentication and pass them to this authorization service
3. **Request your function key** from the administrator to replace `YOUR_GET_AUTHORIZATION_FUNCTION_KEY` in the code examples

---

## Base Configuration

**Base URL:**
```
https://authorizationservice-fghyh8beb6fpa2hk.eastus-01.azurewebsites.net/api
```

---

## Primary Endpoint: Get All Authorization (Recommended)

**Use this endpoint for most applications.** It returns all authorization data in one call, and you can ignore any fields you don't need.

### Request
**URL:** `/get_authorization`  
**Method:** `POST`

**Authentication Header:**
```python
headers = {
    "Content-Type": "application/json",
    "x-functions-key": "YOUR_GET_AUTHORIZATION_FUNCTION_KEY"
}
```

**Body:** *(All fields optional - only send what you need)*
```json
{
  "ADMIN_EMAIL": "user@example.com",
  "APP_ID": 123,
  "EMPLOYEE_CODE": "EMP001"
}
```

### Response
```json
{
  "admin": true,
  "admin_type": "super",
  "App_Security_level": "5",
  "TITLE_GROUP_SECURITY_LEVEL": "50"
}
```

**Response Fields:**
- `admin` - Boolean, true if user is admin for this app
- `admin_type` - String or null, type of admin (e.g., "super", "regular") - can be ignored if null
- `App_Security_level` - String or null, security level required for the app
- `TITLE_GROUP_SECURITY_LEVEL` - String or null, employee's security level (numeric value like "50")

### Python Example
```python
import requests

def get_authorization(email=None, app_id=None, employee_code=None):
    url = "https://authorizationservice-fghyh8beb6fpa2hk.eastus-01.azurewebsites.net/api/get_authorization"
    headers = {
        "Content-Type": "application/json",
        "x-functions-key": "YOUR_GET_AUTHORIZATION_FUNCTION_KEY"
    }
    
    data = {}
    if email and app_id:
        data["ADMIN_EMAIL"] = email
        data["APP_ID"] = app_id
    if app_id:
        data["APP_ID"] = app_id
    if employee_code:
        data["EMPLOYEE_CODE"] = employee_code
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Usage - Get all authorization info
result = get_authorization(
    email="user@example.com",
    app_id=123,
    employee_code="EMP001"
)

# Use only what you need, ignore the rest
if result.get("admin"):
    print("User is admin")
    if result.get("admin_type"):
        print(f"Admin type: {result['admin_type']}")

app_security = result.get("App_Security_level")
if app_security:
    print(f"App requires security level: {app_security}")

employee_security = result.get("TITLE_GROUP_SECURITY_LEVEL")
if employee_security:
    print(f"Employee security level: {employee_security}")
```

---

## Individual Endpoints (Advanced)

Use these endpoints only if you need granular control or have specific performance requirements.

### Endpoint 1: Check Admin Status

### Request
**URL:** `/check_admin`  
**Method:** `POST`

**Body:**
```json
{
  "ADMIN_EMAIL": "user@example.com",
  "APP_ID": 123
}
```

### Response
**If user is admin with type:**
```json
{
  "admin": true,
  "admin_type": "super"
}
```

**If user is admin without type:**
```json
{
  "admin": true,
  "admin_type": null
}
```

**If user is not admin:**
```json
{
  "admin": false,
  "admin_type": null
}
```

### Python Example
```python
import requests

def check_admin(email, app_id):
    url = "https://authorizationservice-fghyh8beb6fpa2hk.eastus-01.azurewebsites.net/api/check_admin"
    headers = {
        "Content-Type": "application/json",
        "x-functions-key": "YOUR_CHECK_ADMIN_FUNCTION_KEY"
    }
    data = {
        "ADMIN_EMAIL": email,
        "APP_ID": app_id
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Usage - Basic check (ignore admin_type)
result = check_admin("user@example.com", 123)
if result["admin"]:
    print("User is admin")
    # admin_type will be present but can be ignored if null

# Usage - Check admin type when needed
result = check_admin("user@example.com", 123)
if result["admin"]:
    admin_type = result.get("admin_type")
    if admin_type:
        print(f"User is admin with type: {admin_type}")
    else:
        print("User is admin (no specific type)")
```

---

### Endpoint 2: Get App Security Level

### Request
**URL:** `/get_app_security_level`  
**Method:** `POST`

**Body:**
```json
{
  "APP_ID": 123
}
```

### Response
```json
{
  "App_Security_level": "5"
}
```

### Python Example
```python
import requests

def get_app_security_level(app_id):
    url = "https://authorizationservice-fghyh8beb6fpa2hk.eastus-01.azurewebsites.net/api/get_app_security_level"
    headers = {
        "Content-Type": "application/json",
        "x-functions-key": "YOUR_GET_APP_SECURITY_LEVEL_FUNCTION_KEY"
    }
    data = {"APP_ID": app_id}
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Usage
result = get_app_security_level(123)
security_level = result["App_Security_level"]
```

---

### Endpoint 3: Get Employee Security Level

### Request
**URL:** `/get_employee_security_level`  
**Method:** `POST`

**Body:**
```json
{
  "EMPLOYEE_CODE": "EMP001"
}
```

### Response
```json
{
  "TITLE_GROUP_SECURITY_LEVEL": "50"
}
```

### Python Example
```python
import requests

def get_employee_security_level(employee_code):
    url = "https://authorizationservice-fghyh8beb6fpa2hk.eastus-01.azurewebsites.net/api/get_employee_security_level"
    headers = {
        "Content-Type": "application/json",
        "x-functions-key": "YOUR_GET_EMPLOYEE_SECURITY_LEVEL_FUNCTION_KEY"
    }
    data = {"EMPLOYEE_CODE": employee_code}
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Usage
result = get_employee_security_level("EMP001")
employee_level = result["TITLE_GROUP_SECURITY_LEVEL"]
```



---

## Session Caching Implementation

### Why Cache?
Avoid calling the authorization service repeatedly for the same user during their session. Cache the results to improve performance and reduce API calls.

### Flask Session Caching Example

```python
from flask import Flask, session
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def get_user_authorization(email, app_id, employee_code=None):
    """
    Get authorization with session caching.
    Checks session first, only calls API if not cached.
    """
    # Check if authorization is already in session
    cache_key = f"auth_{email}_{app_id}"
    
    if cache_key in session:
        return session[cache_key]
    
    # Not in cache, call the API
    url = "https://authorizationservice-fghyh8beb6fpa2hk.eastus-01.azurewebsites.net/api/get_authorization"
    headers = {
        "Content-Type": "application/json",
        "x-functions-key": "YOUR_GET_AUTHORIZATION_FUNCTION_KEY"
    }
    data = {
        "ADMIN_EMAIL": email,
        "APP_ID": app_id
    }
    if employee_code:
        data["EMPLOYEE_CODE"] = employee_code
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    
    # Cache the result in session
    session[cache_key] = result
    session.permanent = True  # Keep session alive
    
    return result

# Usage in route
@app.route('/dashboard')
def dashboard():
    auth = get_user_authorization(
        email=session.get('user_email'),
        app_id=123
    )
    
    if auth['admin']:
        return f"Welcome Admin! Type: {auth['admin_type']}"
    else:
        return "Access denied"

# Clear cache on logout
@app.route('/logout')
def logout():
    session.clear()
    return "Logged out"
```

### Django Session Caching Example

```python
from django.shortcuts import render
import requests

def get_user_authorization(request, email, app_id, employee_code=None):
    """
    Get authorization with session caching.
    """
    cache_key = f"auth_{email}_{app_id}"
    
    # Check session cache
    if cache_key in request.session:
        return request.session[cache_key]
    
    # Call API
    url = "https://authorizationservice-fghyh8beb6fpa2hk.eastus-01.azurewebsites.net/api/get_authorization"
    headers = {
        "Content-Type": "application/json",
        "x-functions-key": "YOUR_GET_AUTHORIZATION_FUNCTION_KEY"
    }
    data = {
        "ADMIN_EMAIL": email,
        "APP_ID": app_id
    }
    if employee_code:
        data["EMPLOYEE_CODE"] = employee_code
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    
    # Cache in session
    request.session[cache_key] = result
    
    return result

# Usage in view
def dashboard_view(request):
    auth = get_user_authorization(
        request,
        email=request.user.email,
        app_id=123
    )
    
    context = {
        'is_admin': auth['admin'],
        'admin_type': auth.get('admin_type')
    }
    return render(request, 'dashboard.html', context)
```

### General Session Caching Pattern

```python
def get_cached_authorization(session_storage, email, app_id, employee_code=None):
    """
    Generic caching pattern for any framework.
    
    Args:
        session_storage: Your framework's session object
        email: User email
        app_id: Application ID
        employee_code: Optional employee code
    
    Returns:
        Authorization data dict
    """
    cache_key = f"auth_{email}_{app_id}"
    
    # 1. Check cache
    if cache_key in session_storage:
        return session_storage[cache_key]
    
    # 2. Call API
    url = "https://authorizationservice-fghyh8beb6fpa2hk.eastus-01.azurewebsites.net/api/get_authorization"
    headers = {
        "Content-Type": "application/json",
        "x-functions-key": "YOUR_GET_AUTHORIZATION_FUNCTION_KEY"
    }
    data = {"ADMIN_EMAIL": email, "APP_ID": app_id}
    if employee_code:
        data["EMPLOYEE_CODE"] = employee_code
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    
    # 3. Store in cache
    session_storage[cache_key] = result
    
    return result
```

---

## Cache Invalidation

### When to Clear Cache

Clear the authorization cache when:
1. **User logs out** - Always clear all session data
2. **Admin permissions change** - If you modify admin status in the database
3. **Session timeout** - Automatic based on your session settings

### Clear Cache Example

```python
# Flask
def clear_auth_cache(email, app_id):
    cache_key = f"auth_{email}_{app_id}"
    session.pop(cache_key, None)

# Django
def clear_auth_cache(request, email, app_id):
    cache_key = f"auth_{email}_{app_id}"
    if cache_key in request.session:
        del request.session[cache_key]

# On logout - clear everything
session.clear()  # Flask
request.session.flush()  # Django
```

---

## Error Handling

All endpoints return errors in this format:
```json
{
  "error": "Error message description"
}
```

### Example Error Handling

```python
def safe_check_admin(email, app_id):
    try:
        result = check_admin(email, app_id)
        
        # Check for error in response
        if "error" in result:
            print(f"API Error: {result['error']}")
            return {"admin": False, "admin_type": None}
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return {"admin": False, "admin_type": None}
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {"admin": False, "admin_type": None}
```

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (missing required parameters)
- `404` - Not Found (record doesn't exist)
- `500` - Internal Server Error (database issues)

---

## Best Practices

1. **Always cache authorization in session** - Don't call the API on every page load
2. **Clear cache on logout** - Security best practice
3. **Handle errors gracefully** - Default to denied access on errors
4. **Use the combined endpoint** (`/get_authorization`) when you need multiple pieces of data
5. **Use individual endpoints** when you only need one specific check
6. **Set appropriate session timeouts** - Balance security with user experience

---

## Quick Start Checklist

- [ ] Add the function key to your environment variables
- [ ] Install `requests` library: `pip install requests`
- [ ] Implement session caching wrapper function
- [ ] Add error handling around API calls
- [ ] Test with your user email and app ID
- [ ] Implement cache clearing on logout
- [ ] Monitor API usage to ensure caching is working
