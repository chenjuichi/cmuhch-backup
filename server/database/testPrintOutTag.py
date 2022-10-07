from tables import User, Reagent, Supplier, Product, Reagent, Grid, InTag, OutTag, Session

import pymysql
from sqlalchemy import exc

# --------------------------

s = Session()
_objects = s.query(OutTag).all()
outStocks = [u.__dict__ for u in _objects]

for product in outStocks:  # 列出產品類別
    print("inTag_id in outTag: ", product['intag_id'])
    _inTag = s.query(InTag).filter_by(id=product['intag_id']).first()
    user = s.query(User).filter_by(id=_inTag.user_id).first()
    reagent = s.query(Reagent).filter_by(id=_inTag.reagent_id).first()
    grid = s.query(Grid).filter_by(id=_inTag.grid_id).first()
    print("data: ", user.emp_name, reagent.reag_id, _inTag.intag_date,
          product['count'], product['unit'], product['outtag_date'], "Grid: ", grid.station, grid.layout, grid.pos)

s.close()
