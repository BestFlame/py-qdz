from flask import Flask, session, redirect, url_for, render_template, request
from flask_login import LoginManager, login_user, logout_user, login_required
from service.user_service import authenticate_user, register_user, update_user_info, change_password, get_user_by_email
from webapi.user import user_bp
from webapi.fastgpt import fastgpt_bp

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(fastgpt_bp)
app.secret_key = 'your-secret-key-here'

# 初始化Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from service.user_service import get_user_by_id
    return get_user_by_id(user_id)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def index():
    return redirect(url_for('login'))

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
            user = get_user_by_email(email)
            login_user(user)
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


# 在这里添加其他路由
if __name__ == '__main__':
    app.run(debug=True)