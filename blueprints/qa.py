from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from decorators import login_required
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    # this is the first method order data according to datetime
    questions = QuestionModel.query.order_by(db.text('-create_time')).all()
    return render_template('index.html', questions=questions)


@bp.route('/question/post', methods=['POST', 'GET'])
@login_required
def post_question():
    if request.method == 'GET':
        return render_template('post_question.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data

            question_model = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question_model)
            db.session.commit()
            return redirect(url_for('qa.index'))
        else:
            flash('the format of the title or content is not correct')
            return redirect(url_for('qa.post_question'))


@bp.route('/question/<int:question_id>')
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template('detail.html', question=question)


@bp.route('/answer/<int:question_id>', methods=['POST'])
@login_required
def answer(question_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        answer_model = AnswerModel(content=content, author=g.user, question_id=question_id)
        db.session.add(answer_model)
        db.session.commit()
        return redirect(url_for('qa.question_detail', question_id=question_id))
    else:
        flash('your comment is too short or an error happened')
        return redirect(url_for('qa.question_detail', question_id=question_id))
