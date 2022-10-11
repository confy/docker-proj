from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def login():
    args = request.args
    
    if args.get('username') == 'admin' and args.get('password') == 'admin':
        return 'Logged in', 200
    
    return 'Invalid credentials', 401
    
if __name__ == '__main__':
    app.run()