from operator import le
from typing import Any, Tuple, Generator

from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.orm.query import Query


class DBManager:
    class DescQuery:
        def __get__(self, instance: "DBManager", owner: type) -> Query:
            return instance.session.query(instance.model)

        def __set__(self, instance: "DBManager", value: Any):
            raise AttributeError("Can't rewrite attribute 'query'")

    query = DescQuery()

    def __init__(self, model: Model, db: SQLAlchemy) -> None:
        self.model = model
        self.session = db.session

    def commit(self, instance: Model) -> Model:
        try:
            self.session.add(instance)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
        return instance

    def create(self, **kwargs) -> Model:
        new_instance = self.model(**kwargs)
        saved_instance = self.commit(new_instance)
        return saved_instance

    def get(self, **kwargs) -> Model:
        return self.query.filter_by(**kwargs).one_or_none()

    def get_or_create(
        self, defaults: dict = None, **kwargs
    ) -> Tuple[Model, bool]:
        if instance := self.query.filter_by(**kwargs).one_or_none():
            return instance, False
        object_fields = kwargs | defaults or {}
        instance = self.create(**object_fields)
        return instance, True

    def update_or_create(
        self, defaults: dict = None, **kwargs
    ) -> Tuple[Model, bool]:
        defaults = {} if defaults is None else defaults
        if instance := self.query.filter_by(**kwargs).one_or_none():
            for field, value in defaults.items():
                setattr(instance, field, value)
            updated_instance = self.commit(instance)
            return updated_instance, False
        object_fields = kwargs | defaults or {}
        instance = self.create(**object_fields)
        return instance, True

    def filter_by(self, **kwargs):
        return self.query.filter_by(**kwargs).all()

    def values(
        self, *args, query: Query = None
    ) -> Generator[dict, None, None]:
        query = self.query if query is None else query
        args = args if args else self.model.__table__.columns.keys()
        entities = [getattr(self.model, arg) for arg in args]
        objects_values = query.with_entities(*entities)
        result = (dict(zip(args, instance)) for instance in objects_values)
        return result

    def all(self):
        return self.query.all()
