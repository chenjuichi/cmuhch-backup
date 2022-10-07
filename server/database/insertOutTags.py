from tables import User, Setting, OutTag, Session

import pymysql
from sqlalchemy import exc

from werkzeug.security import generate_password_hash

# --------------------------

inTag_id = [1, 2, 3, 4, 5, 6, 7]
userID = [2, 3, 4, 5, 6, 7, 7]
count = [1, 1, 1, 1, 2, 5, 2]
unit = ['盒', '盒', '盒', '盒', '盒', '袋', '盒']
outtag_date = ['111/09/12', '111/09/12', '111/08/31', '111/08/31', '111/08/24',
               '111/08/23', '111/08/01', ]

printMark = [False, False, False, False, True, True, True]
stockoutMark = [False, False, False, False, True, True, True]

s = Session()
_results = []

for i in range(7):
    _obj = OutTag(intag_id=inTag_id[i], user_id=userID[i], count=count[i], unit=unit[i],
                  outtag_date=outtag_date[i], isPrinted=printMark[i], isStockout=stockoutMark[i])
    _results.append(_obj)

s.bulk_save_objects(_results)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

s.close()

print("insert 7 outTag data is ok...")
