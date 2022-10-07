from tables import Supplier, Product, Relations, Session

s = Session()
records = s.query(Supplier).all()
for y in records:
    print("record: ", y.product_supplier_id)


s.execute('SET FOREIGN_KEY_CHECKS = 0')
s1 = s.query(Supplier).filter_by(id=1).first()
p1 = s.query(Relations).filter_by(suppier_id_rt=1).all()
for y in p1:
    s.delete(y)
s.delete(s1)
s.commit()
s.execute('SET FOREIGN_KEY_CHECKS = 1')


print(".......")
records = s.query(Supplier).all()
for y in records:
    print("record: ", y.product_supplier_id)

s.close
