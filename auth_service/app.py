from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def login():
    print("Received login request.")
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        if json['username'] == 'admin' and json['password'] == 'admin':
            print("Login was successful.")
            return 'Logged in', 200
    
    print("Login was invalid.")
    return 'Invalid credentials', 401
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
    print("Listening flask app on port 80")