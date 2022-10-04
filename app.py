from flask import Flask, session, g
import config
from exts import db, mail
from blueprints import qa_bp, user_bp
from flask_migrate import Migrate
from models import UserModel

app = Flask(__name__)
app.config.from_object(config)  # pass config object from your config.py file
db.init_app(app)  # bind database and app
mail.init_app(app)  # bind mail service and app

migrate = Migrate(app, db)
# operating command
# flask db init -- initialize database, run once when you run the app in the first time only

# flask db migrate -- generate the new database script, you can add comment with -m 'content',
# you should execute it each time when there are changes to your database model

# flask db upgrade -- upgrade the new table in the database

# join each blueprint, each blueprint need to be registered
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)


# execute following code before each request
@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # allocate g an attr named user and the value is user before
            setattr(g, 'user', user)
            g.user = user
        except:
            pass


# receive request(method and its url) --> execute before_request() --> execute view func according to request
# --> view func return the template --> execute context_processor() --> template rendered
#  following code before each template is rendered and returned
@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        context = {
            'user': g.user
        }
        return context
    else:
        return {}


if __name__ == '__main__':
    app.run()
