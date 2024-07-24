from flask import Flask, jsonify, request
import datetime
import base64

app = Flask(__name__)

# Variable for User store {username: b64 encoded password}
user_store = {}

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({
        "response": "Ok!"
    })

# Post function to check for login
@app.route('/login', methods=['POST'])
def user_login():
    # Obtain data from request
    user_data = request.json
    username = user_data['username']

    # Invalid username scenario
    if username not in user_store:
        return jsonify({
            "message": "Login Denied. Username not found."
        }), 403

    # Get the corresponding details from user store
    user_password = user_store[username]

    # If password matches, return login approved response
    if user_data['password'] == user_password:
        return jsonify({
            "message": "Login Approved. Welcome " + username + ".",
            "username": username,
            "login_time": str(datetime.datetime.now())
        }), 201
    # If password does not match, return login denied response
    else:
        return jsonify({
            "message": "Login Denied. Incorrect username or password."
        }), 403

# Get function to allow GET operation to data service
@app.route('/user_count', methods=['GET'])
def get_data():
    # Return the data store when accessed
    return jsonify({
        "user_count": len(user_store)
    })


def get_credentials():
    credentials = {
        "lucas": "lucas",
        "majd": "majd",
        "marshall": "marshall",
        "punit": "punit",
        "eric": "eric",
        "zexian": "zexian",
        "xuannan": "xuannan",
        "weitian": "weitian",
        "zhiyang": "zhiyang",
        "sriharsha": "sriharsha",
        "shaleen": "shaleen",
        "siddharth": "siddharth",
        "joey": "joey",
        "siang": "siang",
        "chang": "chang",
        "ye": "ye",
        "apoorv": "apoorv",
        "dachi": "dachi",
        "sai": "sai",
        "yan": "yan",
        "peiyao": "peiyao",
        "rui": "rui",
        "sahil": "sahil"
    }
    return credentials

def get_user_store():
    # Get credentails from store
    creds = get_credentials()

    # Encode the passwords
    encoded_credentials = {user: base64.b64encode(password.encode()).decode() for user, password in creds.items()}
    print(encoded_credentials)

    # Return the encoded credentials as user_store
    return encoded_credentials


# Run the app on port 8080
if __name__ == '__main__':
    # Initialize user store
    user_store = get_user_store()

    # Start app on 8080 port
    app.run(debug=True, port=8080, host="0.0.0.0")