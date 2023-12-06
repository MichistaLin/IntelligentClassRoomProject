# exts.py：插件管理
# 扩展的第三方插件

# 1. 导入第三方插件
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 2. 初始化，创建对象
db = SQLAlchemy() # 数据库ORM
migrate = Migrate() # 数据库迁移

# 3. 和app对象关联
def init_exts(app):
	db.init_app(app=app)
	migrate.init_app(app=app, db=db)