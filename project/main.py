from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector

app = FastAPI()
templates = Jinja2Templates(directory="templates")

import os
import mysql.connector
from urllib.parse import urlparse

url = "mysql://root:qMofMrGXLReplCyHZQuHcZJuueAGQuJi@yamabiko.proxy.rlwy.net:15113/railway"

if not url:
    raise Exception("DATABASE_URL is not set ❌")

if isinstance(url, bytes):
    url = url.decode("utf-8")

parsed = urlparse(url)

db_name = parsed.path
if isinstance(db_name, bytes):
    db_name = db_name.decode()
db_name = db_name.lstrip("/")

host = parsed.hostname if parsed.hostname else "localhost"
port = parsed.port if parsed.port else 3306

print("Connecting to:", host, port, db_name)

db = mysql.connector.connect(
    host=host,
    user=parsed.username,
    password=parsed.password,
    database=db_name,
    port=port
)

cursor = db.cursor()

print("Connected successfully ✅")



# Home → redirect to login
@app.get("/")
def home():
    return RedirectResponse("/login")


# Show Register Page
@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )



# Handle Register
@app.post("/register")
def register(
        username: str = Form(...),
        password: str = Form(...),
        name: str = Form(...),
        dob: str = Form(...),
        phone: str = Form(...),
        email: str = Form(...)
):
    query = "INSERT INTO users (username, password, name, dob, phone, email) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (username, password, name, dob, phone, email)

    try:
        cursor.execute(query, values)
        db.commit()
    except:
        return {"message": "Username already exists"}

    return RedirectResponse("/login", status_code=303)


# Show Login Page
# Register page
# Login page
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

# Handle Login
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        return RedirectResponse("/success", status_code=303)
    else:
        return {"message": "Invalid credentials"}


# Success Page
@app.get("/success")
def success(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="success.html"
    )