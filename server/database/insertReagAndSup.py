from tables import Supplier, Product, Reagent, Grid, Session

import pymysql
from sqlalchemy import exc

import faker
faker = faker.Faker(locale='zh_TW')

# --------------------------

# insert
s = Session()

# ---grid table data
#g_reag_id = ['123456789', '234567891', '234567892', '234567893', '234567894']
g_station = ['1', '2', '3', '1', '2', '1', '2',
             '3', '1', '2', '2', '3', '1', '3']  # 1 ~ 3
g_layout = ['4', '4', '1', '2', '3', '5', '4',
            '2', '3', '4', '2', '3', '1', '5']  # 1 ~ 5
g_position = ['6', '1', '1', '2', '5', '6', '8',
              '1', '2', '5', '2', '3', '1', '10']  # 1 ~ 10

G_objects = []
temp_reagent_size = len(g_station)
for i in range(temp_reagent_size):
    g = Grid(
        # reagent_id=g_reag_id[i],
        station=g_station[i],
        layout=g_layout[i],
        pos=g_position[i]
    )
    G_objects.append(g)

s.bulk_save_objects(G_objects)
try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()
# ---

# ---supplier table data
super_id = ['1234',   '1201', '2301', '3401', '2222', '3333', '6767', '2525']
super_name = ['貝克曼', '醫全',  '裕利', '大樹', '實用',  '尚上', '伯昂',  '育聖']
su1 = Supplier(
    super_id=super_id[0],
    super_name=super_name[0],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=faker.numerify("0#-########"))
su2 = Supplier(
    super_id=super_id[1],
    super_name=super_name[1],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=faker.numerify("0#-########"))
su3 = Supplier(
    super_id=super_id[2],
    super_name=super_name[2],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=faker.numerify("0#-########"))
su4 = Supplier(
    super_id=super_id[3],
    super_name=super_name[3],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=faker.numerify("0#-########"))
su5 = Supplier(
    super_id=super_id[4],
    super_name=super_name[4],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=faker.numerify("0#-########"))
su6 = Supplier(
    super_id=super_id[5],
    super_name=super_name[5],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=faker.numerify("0#-########"))
su7 = Supplier(
    super_id=super_id[6],
    super_name=super_name[6],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=faker.numerify("0#-########"))
su8 = Supplier(
    super_id=super_id[7],
    super_name=super_name[7],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=faker.numerify("0#-########"))

s.add_all([su1, su2, su3, su4, su5, su6, su7, su8])
'''
S_objects = []
for i in range(4):
    u = Supplier(
        super_id=super_id[i],
        super_name=super_name[i],
        super_address=faker.address(),
        super_connector=faker.name(),
        # super_tel=faker.phoneNumber().phoneNumber([2-4]0  # -####-####),
        super_tel=faker.numerify("0#-########"),
    )
    S_objects.append(u)
s.bulk_save_objects(S_objects)
'''
try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()
# ---

# ---product table data 產品類別
p1 = Product(name='基因檢測試劑')
p2 = Product(name='核酸萃取試劑')
p3 = Product(name='離心機')
p4 = Product(name='C13檢測試劑')
p5 = Product(name='能力試驗')
p6 = Product(name='教育訓練')
p7 = Product(name='抗血清試劑')
p8 = Product(name='血液諮詢')
p9 = Product(name='Microscan細菌鑑定試劑')
p10 = Product(name='台塑生醫EV71-IgM(rapid-tset)')

s.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

# 供應商資料
records = s.query(Supplier).all()
'''
records[0].product_supplier_id = [p1, p2, p4, p6, p8]
records[1].product_supplier_id = [p1, p2, p3, p7]
records[2].product_supplier_id = [p4, p5, p10]
records[3].product_supplier_id = [p6, p7, p8, p9]
'''
# 將供應商與產品類別做連結
arrays = [p1, p2, p4, p6, p8]
for array in arrays:
    records[0]._products.append(array)
arrays = [p1, p2, p3, p7]
for array in arrays:
    records[1]._products.append(array)
arrays = [p4, p5, p10]
for array in arrays:
    records[2]._products.append(array)
arrays = [p6, p7, p8, p9]
for array in arrays:
    records[3]._products.append(array)
arrays = [p2, p4, p6, p8]
for array in arrays:
    records[4]._products.append(array)
arrays = [p1, p4, p6, p8]
for array in arrays:
    records[5]._products.append(array)
arrays = [p1, p2, p6, p8]
for array in arrays:
    records[6]._products.append(array)
arrays = [p1, p2, p4]
for array in arrays:
    records[7]._products.append(array)

"""
records = s.query(Product).all()
records[0].supplier_id = [su1, su2]
records[1].supplier_id = [su1, su2]
records[2].supplier_id = [su2]
records[3].supplier_id = [su1, su3]
records[4].supplier_id = [su3]
records[5].supplier_id = [su1, su4]
records[6].supplier_id = [su2, su4]
records[7].supplier_id = [su1, su4]
records[8].supplier_id = [su4]
records[9].supplier_id = [su3]
"""
try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

# --------------------------

# ---reagent table data 試劑
reag_id = ['123456789', '234567891', '234567892',
           '234567893', '234567894', '234567897',
           '234567898', '234567899', '214567897',
           '214567898', '214567899', '224567897',
           '224567898', '224567899']
reag_name = ['ABC',   'ABCD',   'A11',    'A12',    'B2233', 'B3344', 'B3345',
             'B3344', 'B3341',  'B3342',  'B3343',  'B3345', 'B3346', 'B3347']
reag_In_unit = ['盒', '盒', '盒', '盒', '盒', '盒',
                '盒', '盒', '盒', '盒', '盒', '盒',
                '盒', '盒']
reag_Out_unit = ['瓶', '瓶', '瓶', '條', '條', '條',
                 '個', '個', '個', '個', '個', '個',
                 '個', '個']
reag_scale = [10, 5, 5, 4, 4, 4, 10, 10, 8, 7, 8, 10, 4, 12]
reag_period = ['111/10/31', '111/12/31',  '111/12/31',
               '112/6/30',  '111/8/31',   '111/8/31',
               '111/8/31',  '111/8/31',   '111/8/31',
               '111/8/31',  '111/8/31', '111/8/31',
               '111/8/31',  '111/8/31']
reag_stock = [1, 1, 0.5, 1, 1, 1, 2, 1, 1, 1,  1,  1,  1,  1]
reag_temp = [0, 0, 0,   0, 1, 1, 1, 2, 0, 0,
             1,  1,  1,  1]  # 0:室溫、1:2~8度C、2:-20度C
super_id = [1, 1, 1,   1, 2, 2, 2, 4, 3, 3,  8,  7,  6,  5]
grid_id = [1, 2, 3,   4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # 試劑存放於不同格位位置

_objects = []
reag_id_size = len(reag_id)
for x in range(reag_id_size):
    u = Reagent(
        reag_id=reag_id[x],
        reag_name=reag_name[x],
        reag_In_unit=reag_In_unit[x],
        reag_Out_unit=reag_Out_unit[x],
        reag_scale=reag_scale[x],
        reag_period=reag_period[x],
        reag_stock=reag_stock[x],
        reag_temp=reag_temp[x],
        # super_id=super_id[x],
        grid_id=grid_id[x]
    )
    _objects.append(u)

s.bulk_save_objects(_objects)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()


reagent_objects = s.query(Reagent).all()
reagents = [u.__dict__ for u in reagent_objects]
i = 1
for reagent in reagents:
    s.query(Reagent).filter(Reagent.id == i).update(
        {"super_id": super_id[i-1]})
    i = i+1

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

s.close()

print("insert 14 grid data is ok...")
print("insert 8 supplier data is ok...")
print("insert 10 product data is ok...")
print("insert 14 reagent data is ok...")
