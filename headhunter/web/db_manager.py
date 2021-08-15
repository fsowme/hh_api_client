from typing import Tuple

from .models import db


class DBManager:
    class DescQuery:
        def __get__(self, instance: "DBManager", owner):
            return instance.session.query(instance.model)

        def __set__(self, instance, value):
            raise AttributeError("Can't rewrite attribute 'query'")

    query = DescQuery()

    def __init__(self, model: db.Model) -> None:
        self.model = model
        self.session = db.session
        # self.query = self.session.query(self.model)

    def commit(self, instance: db.Model) -> db.Model:
        try:
            self.session.add(instance)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
        return instance

    def create(self, **kwargs) -> db.Model:
        new_instance = self.model(**kwargs)
        saved_instance = self.commit(new_instance)
        return saved_instance

    def get_or_create(
        self, defaults: dict = None, **kwargs
    ) -> Tuple[db.Model, bool]:
        if instance := self.query.filter_by(**kwargs).one_or_none():
            return instance, False
        object_fields = kwargs | defaults or {}
        instance = self.create(**object_fields)
        return instance, True

    def update_or_create(
        self, defaults: dict = None, **kwargs
    ) -> Tuple[db.Model, bool]:
        defaults = {} if defaults is None else defaults
        if instance := self.query.filter_by(**kwargs).one_or_none():
            for field, value in defaults.items():
                setattr(instance, field, value)
            updated_instance = self.commit(instance)
            return updated_instance, False
        object_fields = kwargs | defaults or {}
        instance = self.create(**object_fields)
        return instance, True
