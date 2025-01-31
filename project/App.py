from flask import Flask
from flask_security import Security, hash_password
from flask_security.datastore import SQLAlchemyUserDatastore
from model import db, User,Role
from cache import cache
from api import api
from config import DevelopmentConfig
import workers
from flask_cors import CORS
from task import monthly, daily


datastore=SQLAlchemyUserDatastore(db,User,Role)
def create_app():
# Create a Flask app
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    cache.init_app(app)
    celery = workers.celery
    celery.conf.update(
     broker_url= app.config["CELERY_BROKER_URL"],
     result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask
    app.app_context().push()
    app.security = Security(app, datastore)
    
    return app, celery

#Initiating APP
app, celery = create_app()

CORS(app)


#Creating roles and admin
with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name='admin',description="User is an admin")
    datastore.find_or_create_role(name='creator',description="User is a creator")
    datastore.find_or_create_role(name='user',description="User is a user")
    db.session.commit()
    if not datastore.find_user(email="admin@gmail.com"):
        datastore.create_user(username="admin-cosmo",email="admin@gmail.com",password=hash_password("admin"), roles = ["admin"])
        db.session.commit()

from celery.schedules import crontab
import datetime
import pytz
def timee(): 
    return datetime.datetime.now(pytz.timezone('Asia/Calcutta')) 

@celery.on_after_finalize.connect
def monthly_report(sender, **kwargs):
    sender.add_periodic_task(30.0,monthly.s(),name="at 30 sec")
    sender.add_periodic_task(20.0,daily.s(),name="at 20 sec")
    # sender.add_periodic_task(
    #     crontab(hour=17, minute=30, day_of_month="1",nowfun=timee),
    #     monthly.s(),
    # )
    # sender.add_periodic_task(
    #     crontab(hour=1, minute=40, day_of_week="*",nowfun=timee),
    #     daily.s(),
    # )


# Run the app if this file is executed
if __name__ == '__main__':
    app.run(debug=True, port=5001)




# ~/go/bin/Mailhog

# python3 App.py

# npm run serve

# redis-server

# celery -A App.celery worker -l info
# celery -A App.celery beat --max-interval 1 -l info