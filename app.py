import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

load_dotenv()


def create_app():
    from models import db, Subject

    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        os.environ.get('SQLALCHEMY_DATABASE_URI')
        or os.environ.get('DATABASE_URL')
        or 'sqlite:///scholar.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

    db.init_app(app)

    @app.cli.command('init-db')
    def init_db():
        """Initialize the SQLite database (create tables)."""
        with app.app_context():
            db.create_all()
            print('Initialized the database.')

    @app.route('/')
    def index():
        subjects = Subject.query.order_by(Subject.name).all()
        return render_template('index.html', subjects=subjects)

    @app.route('/subjects')
    def subjects_list():
        subjects = Subject.query.order_by(Subject.name).all()
        return render_template('subjects_list.html', subjects=subjects)

    @app.route('/subjects/new', methods=['GET', 'POST'])
    def subject_create():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            if not name:
                flash('Name is required.', 'danger')
                return render_template('subject_form.html', subject=None)
            s = Subject(name=name, description=description)
            db.session.add(s)
            db.session.commit()
            flash('Subject created.', 'success')
            return redirect(url_for('subjects_list'))
        return render_template('subject_form.html', subject=None)

    @app.route('/subjects/<int:subject_id>/edit', methods=['GET', 'POST'])
    def subject_edit(subject_id):
        subject = Subject.query.get_or_404(subject_id)
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            if not name:
                flash('Name is required.', 'danger')
                return render_template('subject_form.html', subject=subject)
            subject.name = name
            subject.description = description
            db.session.commit()
            flash('Subject updated.', 'success')
            return redirect(url_for('subjects_list'))
        return render_template('subject_form.html', subject=subject)

    @app.route('/subjects/<int:subject_id>/delete', methods=['POST'])
    def subject_delete(subject_id):
        subject = Subject.query.get_or_404(subject_id)
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted.', 'success')
        return redirect(url_for('subjects_list'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
