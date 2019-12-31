import time
from utils.core import db
import datetime

class ProduceScript(db.Model):
    __tablename__ = "hotdata"
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    title = db.Column(db.String(127), nullable=False)
    desc = db.Column(db.String(255),nullable=False)
    hotDesc = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(127), nullable=False)
    imgUrl = db.Column(db.String(127),nullable=False)
    create_time = db.Column(db.DateTime, default=int(time.mktime(datetime.datetime.now().timetuple())))
    type_id =db.Column(db.db.Integer(10),default='')
    type_name =db.Column(db.String(64),default='')
    is_new = db.Column(db.Integer(10),default=0)

