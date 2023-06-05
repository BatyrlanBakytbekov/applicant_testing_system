from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note, Skills, Answers, Score, Test
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import sqlite3


tests = Blueprint('tests', __name__)

@tests.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        # Check if the user has already taken the test
        if current_user.has_taken_test:
            return redirect(url_for('views.home'))


        user_skills = Skills.query.filter_by(user_id=current_user.id).first()
        jobs = Note.query.all()

        redirect_flag = False
        keyword = None

        if user_skills is not None:
            for note in jobs:
                if (
                    (user_skills.programminglang and user_skills.programminglang.lower() in note.data.lower()) or
                    (user_skills.engineeringskill and user_skills.engineeringskill.lower() in note.data.lower()) or
                    (user_skills.itskill and user_skills.itskill.lower() in note.data.lower()) or
                    (user_skills.managementskill and user_skills.managementskill.lower() in note.data.lower()) or
                    (user_skills.marketingskill and user_skills.marketingskill.lower() in note.data.lower())
                ):
                    redirect_flag = True
                    keyword = next(
                        (
                            skill.lower()
                            for skill in [
                                user_skills.programminglang,
                                user_skills.engineeringskill,
                                user_skills.itskill,
                                user_skills.managementskill,
                                user_skills.marketingskill,
                            ]
                            if skill and skill.lower() in note.data.lower()
                        ),
                        False
                    )
                    if keyword is not None:
                        break

        if redirect_flag and keyword is not None:
            conn = sqlite3.connect('tests.db')
            c = conn.cursor()
            c.execute("SELECT * FROM {}_test".format(keyword))
            questions = c.fetchall()
            conn.close()
            return render_template('tests.html', keyword=keyword, questions=questions, user=current_user)
        else:
            flash('No matching tests are available.', category='error')
            return render_template('cv.html', user=current_user)


    elif request.method == 'POST':
        current_user.has_taken_test = True
        db.session.commit()


        jobs = Note.query.all()
        keyword = request.form.get('keyword')

        if keyword is None:
            # Handle the case when keyword is not set
            print("No keyword")
            # Redirect or display an error message
            return redirect(url_for('tests.test'))
        
        conn = sqlite3.connect('tests.db')
        test_name = str(keyword.lower() + "_test")
        c = conn.cursor()
        c.execute("SELECT * FROM {}_test".format(keyword.lower()))
        questions = c.fetchall()
        conn.close()
        score = 0

        for question in questions:
            question_id = question[6]
            answer = request.form.get('question' + str(question[6]))
            applicant_answer = str(answer)
            new_answer = Answers(test_name=test_name, question_id=question_id, correct_answer=question[5],applicant_answer=applicant_answer, user_id=current_user.id)
            db.session.add(new_answer)
            

            print(answer)
            if answer == question[5]:
                score += 1

        db.session.commit()

        if ((score / len(questions)) * 100) >= 80:
            passed = True
            position = next((job for job in jobs if keyword.lower() in job.data.lower()), None).title
        else:
            passed = False
            position = None

        score = Score(test_name=test_name, name=current_user.first_name, score=score)
        db.session.add(score)
        db.session.commit()

        return render_template('score.html', score=score, position=position, passed=passed, questions=questions, user=current_user)
    else:
        return render_template('tests.html', questions=questions, user=current_user)

@tests.route('/create_test', methods=['GET', 'POST'])
@login_required
def create_test():
    if request.method == 'GET':
        if current_user.role != 'admin':
            return redirect(url_for('views.home'))
        question_count = int(request.args.get('question_count', 1))
        return render_template("create_test.html", user=current_user, question_count=question_count)

    elif request.method == 'POST':
        test_name = request.form.get('test_name')
        question_count = int(request.form.get('question_count'))

        for i in range(question_count):
            question = request.form.get(f'question_{i+1}')
            option1 = request.form.get(f'option1_{i+1}')
            option2 = request.form.get(f'option2_{i+1}')
            option3 = request.form.get(f'option3_{i+1}')
            option4 = request.form.get(f'option4_{i+1}')
            correct_answer = request.form.get(f'correct_answer_{i+1}')

            new_test = Test(test_name=test_name, question=question, option1=option1, option2=option2, option3=option3, option4=option4, correct_answer=correct_answer)
            db.session.add(new_test)

        db.session.commit()

        flash('Test created successfully!', category="success")

    return render_template('create_test.html', user=current_user)
