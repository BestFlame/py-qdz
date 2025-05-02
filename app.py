from flask import Flask, session, redirect, url_for, render_template, request
from service.user_service import authenticate_user, register_user

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/health')
def health_check():
    return {'status': 'ok'}, 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        result, status = authenticate_user(email, password)
        if status == 200:
            session['user'] = email
            return redirect(url_for('dashboard'))
        return render_template('login.html', error=result.get('error'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        result, status = register_user(email, password)
        if status == 201:
            return redirect(url_for('login'))
        return render_template('register.html', error=result.get('error'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)