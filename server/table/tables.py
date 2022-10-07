from datetime import datetime
from email.policy import default

from sqlalchemy import Column, Float, Integer, String, DateTime, Boolean, func, ForeignKey, create_engine
from sqlalchemy import text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 宣告一個映射, 建立一個基礎類別
BASE = declarative_base()


class User(BASE):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String(6), nullable=False)
    emp_name = Column(String(10), nullable=False)
    password = Column(String(100), nullable=False)
    dep_id = Column(Integer, ForeignKey('department.id'))
    perm_id = Column(Integer, ForeignKey('permission.id'))
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, emp_id={}, emp_name={}, password={}, dep_id={}, perm_id={}".format(
            self.id, self.emp_id, self.emp_name, self.password, self.dep_id, self.perm_id)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'emp_id': self.emp_id,
            'emp_name': self.emp_name,
            'password': self.password,
            'dep_id': self.dep_id,
            'perm_id': self.perm_id,
        }


class Permission(BASE):  # 一對多, "一":permission, "多":user
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    auth_code = Column(Integer, default=0)  # 0:none, 1:admin, 2:user
    auth_name = Column(String(10), default='none')  # 0:none, 1:admin, 2:user
    user_id = relationship('User', backref='permission')  # 設定一對多關聯的"一"
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, auth_code={}".format(self.id, self.auth_code)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'auth_code': self.auth_code,
        }


class Department(BASE):  # 一對多, "一":department, "多":user
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dep_name = Column(String(12), nullable=False)
    user_id = relationship('User', backref='department')  # 設定一對多關聯的"一"
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, dep_name={}".format(self.id, self.dep_name)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'dep_name': self.dep_name,
        }


# 建立連線
###
# 中文字需要 4-bytes 來作為 UTF-8 encoding.
# MySQL databases and tables are created using a UTF-8 with 3-bytes encoding.
# To store 中文字, you need to use the utf8mb4 character set
###
engine = create_engine(
    "mysql+pymysql://root:77974590@localhost:3306/cmuhch?charset=utf8mb4", echo=False)
# 將己連結的資料庫engine綁定到這個session
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    BASE.metadata.create_all(engine)  # 在資料庫中建立表格, 及映射表格內容
