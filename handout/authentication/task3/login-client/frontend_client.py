from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

LOGIN_SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")

# HTML template for the login page
login_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <script>
        async function login(event) {
            event.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const encodedPassword = btoa(password);

            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: encodedPassword
                })
            });

            const result = await response.json();
            if (response.status === 201) {
                document.getElementById('result').textContent = `Login successful! Welcome ${result.username}. Login time: ${result.login_time}`;
            } else {
                document.getElementById('result').textContent = `Login failed: ${result.message}`;
            }
        }
    </script>
</head>
<body>
    <h1>Login</h1>
    <form onsubmit="login(event)">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br><br>
        <button type="submit">Login</button>
    </form>
    <p id="result"></p>
</body>
</html>
'''

# Display the login page upon reaching the / path
@app.route('/')
def index():
    return render_template_string(login_page)

# Healthcheck path for application
@app.route('/client_healthcheck')
def healthcheck():
    return jsonify({
        "response": "Ok!"
    })

# Login service on client
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    # Send the login request to the actual backend server
    try:
        response = requests.post(LOGIN_SERVER_URL + "/login", json={
            'username': username,
            'password': password
        })
        return jsonify(response.json()), response.status_code
    except:
        return jsonify({
            "error": "Invalid server address. Server not reachable."
        }), 400

if __name__ == '__main__':
    print("SERVER URL is -> " + LOGIN_SERVER_URL)
    app.run(debug=True, port=8080, host="0.0.0.0")