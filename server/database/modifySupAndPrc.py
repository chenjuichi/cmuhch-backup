from tables import Supplier, Product, Reagent, Supplier_Product, Session

# --------------------------

# insert
s = Session()


# ---supplier table data
a_super_id = '9090'
a_super_name = '元佑實業'

m_super_id = '1201'
m_super_name = '醫全'


# ---product table data 產品類別
a_p = '放射線醫用器材'

m_p5 = '能力試驗'
m_p6 = '教育訓練'
m_p9 = 'Microscan細菌鑑定試劑'


# 修改供應商資料
t = s.query(Supplier).filter_by(super_id=m_super_id).first()
arr = []
for tt in t._products:
    arr.append(tt.id)
print("arr:", arr)

# --------

query = s.query(Product).filter(Product.id.in_(arr))
for tt in query:
    t._products.remove(tt)
s.commit()

t = s.query(Supplier).filter_by(super_id=m_super_id).first()
arr = []
for tt in t._products:
    arr.append(tt.id)
print("arr:", arr)

# --------

k = s.query(Supplier).filter_by(super_id=m_super_id).first()
p5 = s.query(Product).filter_by(name=m_p5).first()
k._products.append(p5)
p6 = s.query(Product).filter_by(name=m_p6).first()
k._products.append(p6)
p9 = s.query(Product).filter_by(name=m_p9).first()
k._products.append(p9)
s.commit()

t = s.query(Supplier).filter_by(super_id=m_super_id).first()
arr = []
for tt in t._products:
    arr.append(tt.id)
print("arr:", arr)

s.close()
