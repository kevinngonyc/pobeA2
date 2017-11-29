from marshmallow_sqlalchemy import ModelSchema
from . import db

class Base(db.Model):
  """
  Base database model
  """
  __abstract__ = True
  created_at = db.Column(db.DateTime, default = db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default = db.func.current_timestamp())

class Board(Base):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
 
class BoardSchema(ModelSchema):
    class Meta:
        model = Board
        sqla_session = db.session

class Tag(Base):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

class TagSchema(ModelSchema):
    class Meta:
        model = Tag
        sqla_session = db.session

class Element(Base):
    __tablename__ = 'elements'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    board = db.relationship(Board, cascade="all, delete-orphan", single_parent=True)

class ElementSchema(ModelSchema):
    class Meta:
        model = Element
        sqla_session = db.session

class TagElement(Base):
    __tablename__ = 'tagelements'
    id = db.Column(db.Integer, primary_key=True)
    board_element_id = db.Column(db.Integer, db.ForeignKey('elements.id'))
    element = db.relationship(Element, cascade="all, delete-orphan", single_parent=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    tag = db.relationship(Tag, cascade="all, delete-orphan", single_parent=True)

db.create_all()