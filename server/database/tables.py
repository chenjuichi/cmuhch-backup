from datetime import datetime
#from email.policy import default

from sqlalchemy import Table, Column, Float, Integer, String, DateTime, Boolean, func, ForeignKey, create_engine
from sqlalchemy import text
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 宣告一個映射, 建立一個基礎類別
BASE = declarative_base()


# ------------------------------------------------------------------


class User(BASE):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String(6), nullable=False)
    emp_name = Column(String(10), nullable=False)
    password = Column(String(100), nullable=False)
    #password = Column(String(100), default='a12345678')
    dep_id = Column(Integer, ForeignKey('department.id'))
    perm_id = Column(Integer, ForeignKey('permission.id'))
    setting_id = Column(Integer, ForeignKey('setting.id'))
    isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    isOnline = Column(Boolean, default=False)  # false:user不再線上(logout)
    _instocks = relationship('InTag', backref="user")  # 一對多中的 "一"
    _outstocks = relationship('OutTag', backref="user")  # 一對多中的 "一"
    create_at = Column(DateTime, server_default=func.now())
    #instock_id = relationship('InStock', backref='user')

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, emp_id={}, emp_name={}, password={}, dep_id={}, perm_id={}, setting_id={}, isRemoved={}".format(
            self.id, self.emp_id, self.emp_name, self.password, self.dep_id, self.perm_id, self.setting_id, self.isRemoved)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'emp_id': self.emp_id,
            'emp_name': self.emp_name,
            'password': self.password,
            'dep_id': self.dep_id,
            'perm_id': self.perm_id,
            'setting_id': self.setting_id,
            'isRemoved': self.isRemoved,
        }


# ------------------------------------------------------------------


class Permission(BASE):  # 一對多, "一":permission, "多":user
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 0:none, 1:system, 2:admin, 3:member
    auth_code = Column(Integer, default=0)
    # 0:none, 1:system, 2:admin, 3:member
    auth_name = Column(String(10), default='none')
    # 設定一對多關聯的"一"
    # 設定cascade後,可刪除級關連
    # 不設定cascade, 則perm_id為空的, 但沒刪除級關連
    _user = relationship('User', backref='permission')
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


# ------------------------------------------------------------------


class Department(BASE):  # 一對多, "一":department, "多":user
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dep_name = Column(String(12), nullable=False)
    # 設定一對多關聯的"一"
    # 設定cascade後,可刪除級關連
    # 不設定cascade, 則dep_id為空的, 但沒刪除級關連
    _user = relationship('User', backref='department')
    isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, dep_name={}, isRemoved={}".format(self.id, self.dep_name, self.isRemoved)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'dep_name': self.dep_name,
            'isRemoved': self.isRemoved,
        }


# ------------------------------------------------------------------


class Setting(BASE):  # 一對多, "一":permission, "多":user
    __tablename__ = 'setting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    items_per_page = Column(Integer, default=10)
    isSee = Column(String(1), default=text("0"))      # 0:user沒有看去看公告資料
    message = Column(String(30))
    _user = relationship('User', backref='setting')
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, items_per_page={}, isSee={}, message={}".format(self.id, self.items_per_page, self.isSee, self.message)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'items_per_page': self.items_per_page,
            'isSee': self.isSee,
            'message': self.message,
        }


# ------------------------------------------------------------------


class Grid(BASE):
    __tablename__ = 'grid'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station = Column(String(9), nullable=False)
    layout = Column(String(10), nullable=False)
    pos = Column(String(10), nullable=False)
    # reagent table內的資料除, 父子relation切斷, 也會刪除 reagent的資料
    # _reagents_on_grid = relationship(
    #    'Reagent', backref='grid', cascade="all, delete-orphan")
    # reagent table內的資料除, 父子relation切斷, 但不會刪除 reagent的資料
    _reagents_on_grid = relationship(
        'Reagent', backref='grid', cascade="all, delete")
    _instocks = relationship('InTag', backref="grid")  # 一對多中的 "一"
    # isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, station={}, layout={}, pos={}".format(self.id, self.station, self.layout, self.pos)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'station': self.station,
            'layout': self.layout,
            'pos': self.pos,
        }


# ------------------------------------------------------------------


class Reagent(BASE):
    __tablename__ = 'reagent'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reag_id = Column(String(9), nullable=False)
    reag_name = Column(String(10), nullable=False)
    reag_In_unit = Column(String(10), nullable=False)  # 入庫單位
    reag_Out_unit = Column(String(10), nullable=False)  # 出庫單位
    reag_scale = Column(Integer)  # 比例
    reag_period = Column(String(10), nullable=False)  # 效期
    reag_stock = Column(Float)  # 安全存量
    reag_temp = Column(Integer, default=0)  # 0:室溫、1:2~8度C、2:-20度C
    super_id = Column(Integer, ForeignKey('supplier.id'))
    grid_id = Column(Integer, ForeignKey('grid.id'))
    # true: table有資料,  false:table已經刪除該資料
    isRemoved = Column(Boolean, default=True)
    _instocks = relationship('InTag', backref="reagent")  # 一對多中的 "一"

    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, reag_id={}, reag_name={}, reag_In_unit={}, reag_Out_unit={}, reag_scale={}, reag_period={}, reag_stock={}, reag_temp={}, super_id={}, isRemoved={}, create_at={}".format(
            self.id, self.reag_id, self.reag_name, self.reag_In_unit, self.reag_Out_unit, self.reag_scale, self.reag_period, self.reag_stock, self.reag_temp, self.super_id, self.isRemoved, self.create_at)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'reag_id': self.reag_id,
            'reag_name': self.reag_name,
            'reag_In_unit': self.reag_In_unit,
            'reag_Out_unit': self.reag_Out_unit,
            'reag_scale': self.reag_scale,
            'reag_period': self.reag_period,
            'reag_stock': self.reag_stock,
            'reag_temp': self.reag_temp,
            'super_id': self.super_id,
            'isRemoved': self.isRemoved,
            'create_at': self.create_at,
        }


# ------------------------------------------------------------------


class Supplier(BASE):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True, autoincrement=True)
    super_id = Column(String(4), nullable=False)
    super_name = Column(String(40), nullable=False)
    super_address = Column(String(80), nullable=False)
    super_connector = Column(String(10), nullable=False)
    super_tel = Column(String(11), nullable=False)

    _reagents = relationship('Reagent', backref="supplier")

    # a:反向參考 Product.Supplier, b:children objects were getting disassociated (parent set to NULL) before the parent is deleted
    _products = relationship(
        'Product', secondary="supplier_product", back_populates="_suppliers")
    #product_supplier_id = relationship('Product', secondary="relations", backref="supplier", cascade="all, delete")
    isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, super_id={}, super_name={}, super_address={}, super_connector={}, super_tel={}, isRemoved={}".format(
            self.id, self.super_id, self.super_name, self.super_address, self.super_connector, self.super_tel, self.isRemoved)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'super_id': self.super_id,
            'super_name': self.super_name,
            'super_address': self.super_address,
            'super_connector': self.super_connector,
            'super_tel': self.super_tel,
            'isRemoved': self.isRemoved,
            # 'reag_id': self.reag_id,
            # 'super_product': self.super_product,
        }


# ------------------------------------------------------------------


class Supplier_Product(BASE):
    __tablename__ = 'supplier_product'

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    suppier_id = Column(Integer, ForeignKey('supplier.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    #create_at = Column(DateTime, server_default=func.now())


# ------------------------------------------------------------------


class Product(BASE):    # 多對多, "多":product, "多":supplier
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    _suppliers = relationship(
        'Supplier', secondary="supplier_product", back_populates="_products")  # a:反向參考 Product.Supplier, b:children objects were getting disassociated (parent set to NULL) before the parent is deleted
    isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, name={}, isRemoved={}".format(self.id, self.name, self.isRemoved)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'isRemoved': self.isRemoved,
        }


'''
class InStock(BASE):
    __tablename__ = 'instock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    _intags = relationship('InTag', backref='instock')
    #tag_count = Column(Integer, default=1)
    #tag_unit = Column(String(10), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    #updated_at = Column(DateTime, onupdate=func.now())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, tag_id={}, create_at={}, update_at={}".format(self.id, self.tag_id, self.create_at, self.update_at)

    def get_dict(self):
        return {
            'id': self.id,
            'tag_id': self.tag_id,
            # 'tag_count': self.count,
            # 'tag_unit': self.unit,
            'create_at':  self.create_at,
            'updated_at':  self.updated_at
        }
'''

# ------------------------------------------------------------------


class InTag(BASE):
    __tablename__ = 'intag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))        # 一對多中的 "多"
    reagent_id = Column(Integer, ForeignKey('reagent.id'))  # 一對多中的 "多"
    grid_id = Column(Integer, ForeignKey('grid.id'))        # 一對多中的 "多"
    count = Column(Integer, default=1)                # 入(在)庫數量
    stockOut_temp_count = Column(Integer, default=0)  # 暫時領料數 for stockOut計數
    batch = Column(String(20))                        # 批號
    intag_date = Column(String(10), nullable=False)   # 入庫日期

    _outstocks = relationship('OutTag', backref="intag")  # 一對多中的 "一"

    isRemoved = Column(Boolean, default=True)   # false:已經刪除資料
    isPrinted = Column(Boolean, default=False)  # false: 標籤尚未列印, true:已列印
    isStockin = Column(Boolean, default=False)  # false:尚未入庫, true:已入庫

    comment = Column(String(80))  # 盤點說明

    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    create_at = Column(DateTime, server_default=func.now())

    def __repr__(self):  # 定義變數輸出的內容
        # return "id={}, user_id={}, reagent_id={}, count={}, unit={}, grid_id={}".format(self.id, self.user_id, self.reagent_id, self.count, self.unit, self.grid_id)
        return "id={}, user_id={}, reagent_id={}, count={}, grid_id={}".format(self.id, self.user_id, self.reagent_id, self.count, self.grid_id)

    def get_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'reagent_id': self.reagent_id,
            'count': self.count,

            'grid_id': self.grid_id,
        }


# ------------------------------------------------------------------

'''
class OutStock(BASE):
    __tablename__ = 'outstock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    _outtags = relationship('OutTag', backref='outstock')
    #tag_count = Column(Integer, default=1)
    #tag_unit = Column(String(10), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    #updated_at = Column(DateTime, onupdate=func.now())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, tag_id={}, create_at={}, update_at={}".format(self.id, self.tag_id, self.create_at, self.update_at)

    def get_dict(self):
        return {
            'id': self.id,
            'tag_id': self.tag_id,
            # 'tag_count': self.count,
            # 'tag_unit': self.unit,
            'create_at':  self.create_at,
            'updated_at':  self.updated_at
        }
'''

# ------------------------------------------------------------------


class OutTag(BASE):
    __tablename__ = 'outtag'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    intag_id = Column(Integer, ForeignKey('intag.id'))
    user_id = Column(Integer, ForeignKey('user.id'))  # 一對多中的 "多"
    # reagent_id = Column(Integer, ForeignKey('reagent.id'))  # 一對多中的 "多"
    # grid_id = Column(Integer, ForeignKey('grid.id'))  # 一對多中的 "多"
    # indate_id = Column(String(10), nullable=False)  # 入庫日期

    count = Column(Integer, default=1)  # 數量
    unit = Column(String(10), nullable=False)  # 單位
    outtag_date = Column(String(10), nullable=False)    # 領用日期

    # true:已領料, 準備列印標籤; false:已領料, 且刪單
    isRemoved = Column(Boolean, default=True)
    isPrinted = Column(Boolean, default=False)    # false: 標籤尚未列印, true:已列印
    # false:尚未出庫(在庫), true:已出庫(領料)
    isStockout = Column(Boolean, default=False)

    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    create_at = Column(DateTime, server_default=func.now())

    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, intag_id={}, count={}, unit={}, outtag_date={}".format(self.id, self.intag_id, self.count, self.unit, self.outtag_date)

    def get_dict(self):
        return {
            'id': self.id,
            'intag_id': self.intag_id,
            'count': self.count,
            'unit': self.unit,
            'outtag_date': self.outtag_date,
        }


# ------------------------------------------------------------------


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
    print("table creating is ok...")
