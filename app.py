from flask import Flask, render_template, request
import json
import requests
import traceback

app = Flask(__name__, template_folder="templates")

HOST = "http://127.0.0.1:5000"

@app.route("/signin", methods=["GET", "POST"])
def signin():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            endpoint = f'{HOST}/auth/api_key'
            payload = {
                "username": username, 
                "password": password
            }
            try:
                response = requests.get(endpoint, json=payload).text
            except:
                return render_template("signin.html", error="Failed to connect to host.")
            data = json.loads(response)
            if 'error' in data:
                return render_template("signin.html", error=data['error'])
            else:
                api_key = data["api_key"]
                return render_template("api_key.html", username=username, api_key=api_key)
        return render_template("signin.html")
    except:
        traceback.print_exc()
        return render_template("signin.html", error="Something went wrong")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            endpoint = f'{HOST}/users/create'
            payload = {
                "username": username, 
                "password": password,
                "confirm_password": confirm_password
            }
            if password != confirm_password:
                return render_template("signup.html", error="Passwords don't match.")
            try:
                response = requests.post(endpoint, json=payload).text
            except:
                return render_template("signup.html", error="Failed to connect to host.")
            data = json.loads(response)
            if 'error' in data:
                if 'exists' in data['error']:
                    return render_template("signup.html", username=username)
                return render_template("signup.html", error=data['error'])
            else:
                api_key = data["api_key"]
                return render_template("api_key.html", username=username, api_key=api_key)
        return render_template("signup.html")
    except:
        traceback.print_exc()
        return render_template("signup.html", error="Something went wrong")

if __name__ == "__main__":
    app.run(port=5002)