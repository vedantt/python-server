from db import db
from db import JsonEncodedDict

class callbackModel(db.Model):
    __tablename__ = 'items'

    keys = db.Column(db.String())
    method = db.Column(db.String())
    data = db.Column(JsonEncodedDict)
    header = db.Column(JsonEncodedDict)
    url = db.Column(db.String())
    time = db.Column(db.String())
    state = db.Column(db.String(), default=True)
    id = db.Column(db.Integer , primary_key=True)

    def __init__(self, keys,method, data,headers,url,time,state):
        self.keys = keys
        self.method = method
        self.data = data
        self.header = headers
        self.url = url
        self.time = time
        self.state = state
    def json(self):
        return {
            'methoda': self.method,
            'data': self.data,
            'header': self.header,
            'url': self.url,
            'time': self.time,
            'state': self.state
                }

    @classmethod
    def find_by_key(cls, keys):
        return cls.query.filter_by(keys=keys).all()
    @classmethod
    def delete_all_db(cls):
        try:
            cls.query(callbackModel).delete()
            db.session.commit()
        except: pass
        return


    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
