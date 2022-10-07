from flask import Blueprint, jsonify, request
from sqlalchemy import func
from database.tables import User, Reagent, Supplier, Product, Permission, Department, Grid, OutTag, InTag, Setting, Session

from werkzeug.security import generate_password_hash

createTable = Blueprint('createTable', __name__)


# ------------------------------------------------------------------

# create user data and perm.id=1 into table
@createTable.route("/register", methods=['POST'])
def register():
    print("register....")
    request_data = request.get_json()

    emp_id = (request_data['emp_id'] or '')
    emp_name = (request_data['emp_name'] or '')
    sPWD = (request_data['password'] or '')  # convert null into empty string

    return_value = True  # true: 資料正確, 註冊成功
    if emp_id == "" or emp_name == "" or sPWD == "":
        return_value = False  # false: 資料不完全 註冊失敗

    dep = (request_data['dep'] or '')  # convert null into empty string
    # code = request_data['perm_id']

    s = Session()
    department = s.query(Department).filter_by(dep_name=dep).first()
    if not department:
        return_value = False  # if the user's department does not exist

    # permission = s.query(Permission).filter_by(auth_code=code).first()
    # if not permission:
    #    return_value = False  # if the user's permission does not exist

    old_user = s.query(User).filter_by(emp_id=emp_id).first()
    if old_user:
        return_value = False  # if the user exist

    if return_value:
        # kk_setting = Setting(message='hello ' + emp_name)
        new_user_setting = Setting(
            message='hello ' + emp_name,)
        s.add(new_user_setting)
        s.flush()
        new_user = User(emp_id=emp_id,
                        emp_name=emp_name,
                        password=generate_password_hash(sPWD, method='sha256'),
                        dep_id=department.id,
                        # perm_id=permission.id,
                        perm_id=1,  # first permission,auth_code=0:none
                        setting_id=new_user_setting.id,)
        s.add(new_user)

        s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })


# create user data and perm.id=4 into table
@createTable.route("/createUser", methods=['POST'])
def createUser():
    print("createUser....")
    request_data = request.get_json()

    emp_id = (request_data['emp_id'] or '')
    emp_name = (request_data['emp_name'] or '')
    sPWD = (request_data['password'] or '')  # convert null into empty string

    return_value = True  # true: 資料正確, 註冊成功
    if emp_id == "" or emp_name == "" or sPWD == "":
        return_value = False  # false: 資料不完全 註冊失敗

    dep = (request_data['dep'] or '')  # convert null into empty string
    # code = request_data['perm_id']

    s = Session()
    department = s.query(Department).filter_by(dep_name=dep).first()
    if not department:
        return_value = False  # if the user's department does not exist

    # permission = s.query(Permission).filter_by(auth_code=code).first()
    # if not permission:
    #    return_value = False  # if the user's permission does not exist

    old_user = s.query(User).filter_by(emp_id=emp_id).first()
    if old_user:
        return_value = False  # if the user exist

    if return_value:
        new_user_setting = Setting(
            message='add ' + emp_name,)
        s.add(new_user_setting)
        s.flush()
        new_user = User(emp_id=emp_id,
                        emp_name=emp_name,
                        password=generate_password_hash(sPWD, method='sha256'),
                        dep_id=department.id,
                        # perm_id=permission.id,
                        perm_id=4,  # first permission,auth_code=0:none
                        setting_id=new_user_setting.id,)
        s.add(new_user)
        s.commit()

    s.close()
    return jsonify({
        'status': return_value,
    })


# create reagent data table
@createTable.route("/createReagent", methods=['POST'])
def create_reagent():
    print("createReagent....")
    request_data = request.get_json()

    _id = request_data['reag_id']
    _name = request_data['reag_name']
    _in_unit = request_data['reag_In_unit']
    _out_unit = request_data['reag_Out_unit']
    _scale = request_data['reag_scale']
    _period = request_data['reag_period']
    _stock = request_data['reag_stock']
    _temp = request_data['reag_temp']

    return_value = True  # true: 資料正確, 註冊成功
    if _id == "" or _name == "" or _in_unit == "" or _out_unit == "" or _scale == "" or _period == "" or _stock == "" or _temp == "":
        return_value = False  # false: 資料不完全 註冊失敗

    # convert null into empty string
    _supplier = (request_data['reag_supplier'] or '')

    s = Session()

    supplier = s.query(Supplier).filter_by(super_name=_supplier).first()
    if not supplier:
        return_value = False  # if the reagent's supplier does not exist

    old_reagent = s.query(Reagent).filter_by(reag_id=_id).first()
    if old_reagent:
        return_value = False  # if the user exist

    if return_value:
        _scale = int(_scale)
        _stock = float(_stock)

        if _temp == '室溫':  # 0:室溫、1:2~8度C、2:-20度C
            k1 = 0
        if _temp == '2~8度C':
            k1 = 1
        if _temp == '-20度C':
            k1 = 2

        new_reagent = Reagent(reag_id=_id, reag_name=_name,
                              reag_In_unit=_in_unit, reag_Out_unit=_out_unit,
                              reag_period=_period,   reag_scale=_scale,
                              reag_stock=_stock, reag_temp=k1, super_id=supplier.id)
        s.add(new_reagent)
        s.commit()

    s.close()
    return jsonify({
        'status': return_value
    })


# create grid data table
@createTable.route("/createGrid", methods=['POST'])
def create_grid():
    print("createGrid....")
    request_data = request.get_json()

    _id = request_data['grid_id']
    _reagID = request_data['grid_reagID']
    _reagName = request_data['grid_reagName']
    _station = request_data['grid_station']
    _layout = request_data['grid_layout']
    _pos = request_data['grid_pos']

    data_check = (True, False)[_id == "" or _reagID == "" or _reagName == ""]
    # return_value = True  # true: 資料正確, 註冊成功
    # if _id == "" or _reagID == "" or _reagName == "":
    #    return_value = False  # false: 資料不完全 註冊失敗

    return_value = False
    if data_check:
        s = Session()
        # targid grid
        target_grid = s.query(Grid).filter_by(station=_station,
                                              layout=_layout, pos=_pos).first()
        # return_value = False
        if not target_grid:
            # new grid
            new_grid = Grid(station=_station, layout=_layout, pos=_pos)
            s.add(new_grid)
            s.flush()
            s.query(Reagent).filter(Reagent.reag_id ==
                                    _reagID).update({"grid": new_grid.id})
            s.commit()
            return_value = True

        s.close()

    return jsonify({
        'status': return_value
    })


# create supplier data table
@createTable.route("/createSupplier", methods=['POST'])
def create_supplier():
    print("createSupplier....")
    request_data = request.get_json()

    _supID = request_data['sup_id']
    _supName = request_data['sup_name']
    _supAddress = request_data['sup_address']
    _supContact = request_data['sup_contact']
    _supPhone = request_data['sup_phone']
    _supProducts = request_data['sup_products']
    #print("_supProducts: ", _supProducts)

    data_check = (True, False)[_supID == "" or _supName ==
                               "" or _supAddress == "" or _supContact == "" or _supPhone == "" or len(_supProducts) == 0]

    return_value = True  # true: 資料正確, 註冊成功
    if not data_check:
        return_value = False  # false: 資料不完全 註冊失敗

    s = Session()

    old_supplier = s.query(Supplier).filter_by(super_id=_supID).first()
    if old_supplier:
        return_value = False  # if the supplier exist

    if return_value:
        new_supplier = Supplier(super_id=_supID, super_name=_supName,
                                super_address=_supAddress, super_connector=_supContact, super_tel=_supPhone)

        s.add(new_supplier)
        s.flush()

        for array in _supProducts:
            target = s.query(Product).filter_by(id=array).first()
            new_supplier._products.append(target)

        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# create product data table
@createTable.route("/createProduct", methods=['POST'])
def create_product():
    print("createProduct....")
    request_data = request.get_json()

    _prdName = request_data['prd_name']

    data_check = (True, False)[_prdName == ""]

    return_value = True   # true: create資料成功, false: create資料失敗
    if not data_check:    # false: 資料不完全
        return_value = False

    s = Session()

    old_product = s.query(Product).filter_by(name=_prdName).first()
    if old_product:
        return_value = False  # the product record had existed

    if return_value:
        new_product = Product(name=_prdName)

        s.add(new_product)
        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# create department data table
@createTable.route("/createDepartment", methods=['POST'])
def create_department():
    print("createDepartment....")
    request_data = request.get_json()

    _emp_dep = (request_data['emp_dep'] or '')

    data_check = (True, False)[_emp_dep == ""]

    return_value = True   # true: create資料成功, false: create資料失敗
    if not data_check:    # false: 資料不完全
        return_value = False

    s = Session()
    old_department = s.query(Department).filter_by(dep_name=_emp_dep).first()
    if old_department:
        return_value = False  # the product record had existed

    if return_value:
        new_department = Department(dep_name=_emp_dep)
        s.add(new_department)
        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# create stockout data into table
@createTable.route("/createStockOut", methods=['POST'])
def create_stockOut():
    print("createStockOut....")
    request_data = request.get_json()

    _data = request_data['stockOut_array']
    _count = request_data['stockOut_count']

    # print("_data, _count: ", _data, _count)
    return_array = []
    return_value = True  # true: 資料正確
    if not _data or len(_data) != _count:
        return_value = False  # false: 資料不完全

    s = Session()

    # _objects = s.query(OutTag).all()
    # _outtags = [u.__dict__ for u in _objects]
    # print("_objects, _outtags: ", type(_objects), type(_outtags))
    # cnt1 = len(_objects)
    # cnt2 = len(_data)
    # print("cnt1, cnt2: ", cnt1, cnt2)
    '''
    for i in range(cnt1):
        result1 = list(_outtags[i].keys())
        for j in range(cnt2):
            result2 = list(_data[j].keys())
            # if outtagKey in _data.keys():
            print("compare Key1: ", result1)
            print("compare Key2: ", result2)
    '''
    _user = s.query(User).filter_by(
        emp_name=_data[0]['stockOutTag_Employer']).first()

    for i in range(_count):
        new_outtag = OutTag(intag_id=_data[i]['stockOutTag_InID'],
                            user_id=_user.id,
                            count=_data[i]['stockOutTag_cnt'],
                            unit=_data[i]['stockOutTag_unit'],
                            outtag_date=_data[i]['stockOutTag_Date'],
                            )
        s.add(new_outtag)  # 新增一筆出庫資料
        s.flush()
        # print("outtag add, id: ", new_outtag.id)
        return_array.append(new_outtag.id)

        cursor = s.query(func.sum(OutTag.count)).filter(
            OutTag.intag_id == _data[i]['stockOutTag_InID']).filter(
            OutTag.isRemoved == True)
        total = cursor.scalar()
        # print("total: ", total)

        intag = s.query(InTag).filter_by(
            id=_data[i]['stockOutTag_InID']).first()
        # intag.count = intag.count - _data[i]['stockOutTag_cnt']  # 修改入庫資料
        # intag.stockOut_temp_count = intag.stockOut_temp_count + \
        #    _data[i]['stockOutTag_cnt']  # 修改入庫資料
        intag.stockOut_temp_count = total  # 修改入庫資料

        s.commit()
    s.close()

    return jsonify({
        'status': return_value,
        'return_outTag_ID': return_array,
    })


'''


for key in Boys.keys():
    if key in Dict.keys():
        print True
    else:
        print False

    s = Session()
    if return_value:
        _objects = s.query(OutTag).all()
        for outtagKey in _objects.keys():
            if outtagKey in _data.keys():

            new_department = OutTag(dep_name=_emp_dep)
            s.add(new_department)
            s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })
'''
