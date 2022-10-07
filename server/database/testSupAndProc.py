from tables import Supplier, Product, Reagent, Grid, Session

import pymysql
from sqlalchemy import exc

# --------------------------

s = Session()
products = s.query(Product).all()

for product in products:  # 列出產品類別
    print("*: ", product.name)
    # print(product._suppliers)
    for supplier in product._suppliers:  # 列出供應商
        print("--> ", supplier.super_name)
        for reagent in supplier._reagents:  # 列出該供應商的所有試劑編號
            print(reagent.reag_id)
    print('---')

s.close()
