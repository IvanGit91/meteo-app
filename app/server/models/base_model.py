from datetime import datetime
from app.server import db


class BaseModel:
    def __init__(self):
        self.created_at = datetime.now()

    @classmethod
    def get_columns(cls, to_exclude=None):
        items = vars(cls).items()
        return {k: v for k, v in items if hasattr(v, 'is_attribute') and v.is_attribute and (to_exclude is None or k not in to_exclude)}

    @classmethod
    def get_columns_exclude_basic(cls):
        return cls.get_columns(['id', 'created_at', 'updated_at'])

    @staticmethod
    def commit():
        db.session.commit()

    def save_or_update(self):
        if self.id is None:
            self.save()
        else:
            self.update()

    def save(self):
        db.session.add(self)
        BaseModel.commit()

    def update(self):
        BaseModel.commit()

    def delete(self):
        db.session.delete(self)
        BaseModel.commit()

    def serialize(self, *to_exclude):
        serialized = {}
        for c in self.get_columns():
            if c not in to_exclude:
                serialized[c] = getattr(self, c)
        return serialized

    @classmethod
    def save_all(cls, list_to_save):
        db.session.add_all(list_to_save)
        BaseModel.commit()
        
    @classmethod
    def save_row(cls, row_to_save):
        db.session.add(row_to_save)
        BaseModel.commit()

    @classmethod
    def truncate(cls):
        db.session.query(cls).delete()
        BaseModel.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)
