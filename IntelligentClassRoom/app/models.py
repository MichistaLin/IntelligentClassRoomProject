# models.py：数据库模型
from .exts import db


# 1. 定义模型类：必须继承db.Model
class Temp(db.Model):
	# 表名 温度
	__tablename__ = 'temp'
	# 定义表中的字段
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	temperature = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, nullable=False)


class Humid(db.Model):
	# 表名 湿度
	__tablename__ = 'humid'
	# 定义表中的字段
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	humidity = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, nullable=False)


class Airp(db.Model):
	# 表名 气压
	__tablename__ = 'airp'
	# 定义表中的字段
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	air_pressure = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, nullable=False)


class Light(db.Model):
	# 表名 光照
	__tablename__ = 'light'
	# 定义表中的字段
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	light = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, nullable=False)