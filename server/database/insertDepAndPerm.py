from tables import Permission, Department, Session

import pymysql
from sqlalchemy import exc

# --------------------------

s = Session()

#新增 Department table資料
dep_name = "檢驗科"
new_dep = Department(dep_name=dep_name)
s.add(new_dep)

dep_name = "醫事科"
new_dep = Department(dep_name=dep_name)
s.add(new_dep)

dep_name = "護理科"
new_dep = Department(dep_name=dep_name)
s.add(new_dep)

dep_name = "麻醉科"
new_dep = Department(dep_name=dep_name)
s.add(new_dep)

dep_name = "機器人推進部"
new_dep = Department(dep_name=dep_name)
s.add(new_dep)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()


print("insert 5 department data is ok...")

# --------------------------

#新增 Permission table資料
auth_code = 0
auth_name = "none"
new_perm = Permission(auth_code=auth_code, auth_name=auth_name)
s.add(new_perm)

auth_code = 1
auth_name = "system"
new_perm = Permission(auth_code=auth_code, auth_name=auth_name)
s.add(new_perm)

auth_code = 2
auth_name = "admin"
new_perm = Permission(auth_code=auth_code, auth_name=auth_name)
s.add(new_perm)

auth_code = 3
auth_name = "member"
new_perm = Permission(auth_code=auth_code, auth_name=auth_name)
s.add(new_perm)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

s.close()

print("insert 3 type permission data is ok...")
