# coding=utf-8
# Created 2014 by Janusz Skonieczny
import logging
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db():
    logging.debug("db.create_all")
    db.create_all()
