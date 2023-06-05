from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Skills
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


skills = Blueprint('skills', __name__)

@skills.route('/cv', methods=['GET', 'POST'])
@login_required
def cv():
    if request.method == "POST":
        programming_language = request.form.get('ProgrammingLanguage')
        engineering_skill = request.form.get('EngineeringSkill')
        it_skill = request.form.get('ITSkill')
        management_skill = request.form.get('ManagementSkill')
        marketing_skill = request.form.get('MarketingSkill')

        skills = Skills(
            programminglang=programming_language,
            engineeringskill=engineering_skill,
            itskill=it_skill,
            managementskill=management_skill,
            marketingskill=marketing_skill,
            user_id=current_user.id
        )
        
        db.session.add(skills)
        db.session.commit()

        flash('All done! Filled skills are saved', category='success')
    return render_template("cv.html", user=current_user )


