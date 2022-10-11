from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def login(body):
    if body['username'] == 'admin' and body['password'] == 'admin':
        return 'Logged in', 200
    
    return 'Invalid credentials', 401
    
if __name__ == '__main__':
    app.run()