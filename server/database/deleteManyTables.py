from tables import User, Permission, Department, Setting, Session, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, DateTime, Boolean, func, ForeignKey, create_engine
from sqlalchemy import MetaData

s = Session()


def drop_table(table_name):
   #engine = create_engine(URL(**DATABASE))
    base = declarative_base()
    #metadata = MetaData(engine, reflect=True)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables.get(table_name)
    if table is not None:
        print("Deleting", table_name, "table")
        base.metadata.drop_all(engine, [table], checkfirst=True)


s.execute('SET FOREIGN_KEY_CHECKS = 0')
drop_table('outtag')       # 待入庫table
drop_table('intag')       # 待入庫table

drop_table('user')        # 員工table
drop_table('permission')  # 權限table
drop_table('department')  # 部門table
drop_table('setting')     # 部門table

drop_table('reagent')     # 試劑table
drop_table('grid')        # 格位table

drop_table('supplier_product')
drop_table('product')           # 產品類別table
drop_table('supplier')          # 供應商table

drop_table('outtag')      # 出庫table
drop_table('outstock')    # 出庫table

s.execute('SET FOREIGN_KEY_CHECKS = 1')

s.close()

print("delete 9 tables is ok...")
