from flask import Blueprint, render_template

fastgpt_bp = Blueprint('fastgpt', __name__, url_prefix='/fastgpt', template_folder='../templates/fastgpt')

@fastgpt_bp.route('/team')
def team_management():
    return render_template('fastgpt_team.html')

@fastgpt_bp.route('/user')
def user_management():
    return render_template('fastgpt_user.html')