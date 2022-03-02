from db import db
from db import JsonEncodedDict
from datetime import datetime, timedelta


class callbackModel(db.Model):
    __tablename__ = 'items'

    keys = db.Column(db.String(), primary_key=True)
    batch_number = db.Column(db.String())
    price = db.Column(db.Integer())
    location = db.Column(db.String())
    feature = db.Column(db.String())
    # data = db.Column(JsonEncodedDict)
    time = db.Column(db.Date(), default=datetime.now().date())
    state = db.Column(db.String(), default="ACTIVE")
    quantity = db.Column(db.Integer, default=-999)
    id = db.Column(db.Integer, primary_key=True)
    recheck = db.Column(db.Boolean, default=False)
    broken = db.Column(db.Boolean, default=False)
    missing = db.Column(db.Boolean, default=False)
    category = db.Column(db.String())
    update_date = db.Column(db.Date(), default=datetime.now().date())
    extra = db.Column(db.String())

    def __init__(self, keys, feature, location, price, batch_number, id, time, state, quantity, category):
        self.keys = keys
        self.feature = feature
        self.location = location
        self.batch_number = batch_number
        self.price = price
        self.time = time
        self.state = state
        self.id = id
        self.quantity = quantity
        self.category = category
        self.update_date = time
        self.extra = "extra"

    def json(self):
        return {
            'NAME': self.keys,
            'FEATURE': self.feature,
            'LOCATION': self.location,
            'BATCH NUMBER': self.batch_number,
            'CREATION_DATE': str(self.time),
            'PRICE': self.price,
            'BOX NO': self.id,
            'STATE': self.state,
            'QUANTITY': self.quantity,
            "CATEGORY": self.category,
            'RECHECK': self.recheck,
            'MISSING': self.missing,
            'BROKEN': self.broken,
            'UPDATED_DATE': str(self.update_date),
            'EXTRA': self.extra
        }

    @classmethod
    def find_by_key(cls, keys, state):
        return cls.query.filter_by(keys=keys).filter_by(state=state).all()

    @classmethod
    def find_by_only_key(cls, keys):
        return cls.query.filter_by(keys=keys).all()

    @classmethod
    def find_and_update_name(cls, keys, updated_name):
        items = cls.query.filter_by(keys=keys).all()
        for each in items:
            each.keys = updated_name
        db.session.commit()
        return items

    @classmethod
    def find_by_key_and_id(cls, keys, id):
        return cls.query.filter_by(id=id).filter_by(keys=keys).all()

    @classmethod
    def find_all(cls):
        item_name = set()
        item_name_with_category = set()
        item_largest_box_size = {}
        item_stock = {}
        item = cls.query.all()
        for each in item:
            item_name.add(each.keys)
            item_name_with_category.add(each.keys + ':' + each.category)
            if each.keys in item_largest_box_size:
                if each.id > item_largest_box_size[each.keys]:
                    item_largest_box_size[each.keys] = each.id
            else:
                item_largest_box_size[each.keys] = each.id

            if each.state == "ACTIVE":
                if each.keys in item_stock:
                    item_stock[each.keys] = item_stock[each.keys] + 1
                else:
                    item_stock[each.keys] = 1

        return item_name, item_largest_box_size, item_stock, item_name_with_category

    @classmethod
    def find_all_for_delete(cls):
        item_name = set()
        item = cls.query.all()
        return item

    @classmethod
    def find_all_data(cls):
        item = cls.query.all()
        return item

    @classmethod
    def find_and_update_state(cls, keys, id, quantity, time):
        item = cls.query.filter_by(id=id).filter_by(keys=keys).first()
        if item.state == "INACTIVE":
            return "Item already deleted"
        if item.quantity != -999:
            if quantity < 0:
                return "please enter positive quantity to be reduced" + str(item)
            item.quantity = item.quantity - quantity
            if item.quantity == 0:
                item.state = "INACTIVE"
                item.update_date = time
                db.session.commit()
            if item.quantity < 0:
                return "please enter value based on the box value not the total order value" + str(item)
            item.feature = item.feature + ",SALE#" + str(time) + ":" + str(quantity)
            item.update_date = time
            db.session.commit()
            return "item quantity reduced from the box" + str(item)
        if item.quantity == -999 and quantity != -999:
            return "PLEASE ENTER 0 IN QUANTITY"
        item.feature = item.feature + ",SALE#" + str(time) + ":" + str(quantity)
        item.state = "INACTIVE"
        item.update_date = time
        db.session.commit()
        return item

    @classmethod
    def find_all_changes_done_today(cls):
        item = cls.query.filter(cls.update_date > (datetime.now().date() - timedelta(days=2))).all()
        return item

    @classmethod
    def find_by_only_key_and_update_godown(cls, keys, location):
        items = cls.query.filter_by(keys=keys).all()
        for each in items:
            each.location = location
        db.session.commit()
        return items

    @classmethod
    def find_and_reactivate_record(cls, keys, id, time, state, quantity):
        item = cls.query.filter_by(id=id).filter_by(keys=keys).first()
        item.state = state
        item.feature = item.feature + ",REPURCHASED#" + str(time) + ":" + str(quantity)
        item.update_date = time
        if item.quantity != -999:
            item.quantity = item.quantity + quantity
        db.session.commit()
        return item

    @classmethod
    def find_and_update_record(cls, keys, feature, location, price, batch_number, id, time, state, quantity, category,
                               updated_name, updated_box):
        item = cls.query.filter_by(id=id).filter_by(keys=keys).first()
        item.keys = updated_name
        item.state = state
        item.feature = feature
        item.location = location
        item.batch_number = batch_number
        item.price = price
        item.update_date = time
        item.quantity = quantity
        item.category = category
        item.id = updated_box
        value = db.session.commit()
        return value

    @classmethod
    def set_recheck(cls, datepassed):
        item = cls.query.filter(cls.update_date < datepassed).filter_by(state="ACTIVE").all()
        item_name = set()
        for each in item:
            item_name.add(each.keys + ':' + each.category)
            if not each.recheck:
                each.recheck = True
        item = cls.query.filter(cls.update_date > datepassed).all()
        for each in item:
            if each.recheck:
                each.recheck = False
        db.session.commit()
        return item_name

    @classmethod
    def reportItem(cls, keys, id, operation):
        item = cls.query.filter_by(id=id).filter_by(keys=keys).first()
        if item != None:
            if operation.upper() == "BROKEN":
                item.broken = True
                item.update_date = datetime.now().date()
            elif operation.upper() == "MISSING":
                item.missing = True
                item.update_date = datetime.now().date()
            elif operation.upper() == "FOUND":
                item.missing = False
                item.update_date = datetime.now().date()
            elif operation.upper() == "RECHECKED":
                item.recheck = False
                item.update_date = datetime.now().date()
            else:
                return "operation not supported yet on item " + str(item)
            db.session.commit()
            return item.keys
        return "item not found"

    def save_to_db(self):
        item = db.session.add(self)
        db.session.commit()
        return

    def delete_from_db(self):
        db.session.delete(self)
        with db.engine.begin() as conn:
            conn.execute("VACUUM")
        db.session.commit()
