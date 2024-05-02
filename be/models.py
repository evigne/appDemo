from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    children = db.relationship('Node')
    properties = db.relationship('NodeProperty', backref='node')

class NodeProperty(db.Model):
    __tablename__ = 'node_properties'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.Numeric, nullable=False)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())