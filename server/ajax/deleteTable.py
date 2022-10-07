from flask import Blueprint, jsonify, request
from sqlalchemy import func

from database.tables import User, Reagent, Grid, Supplier, Product, Department, OutTag, InTag, Session

#from werkzeug.security import generate_password_hash

deleteTable = Blueprint('deleteTable', __name__)


# ------------------------------------------------------------------


@deleteTable.route("/removeUser", methods=['POST'])
def remove_user():
    print("removeUser....")
    request_data = request.get_json()
    userID = request_data['ID']

    return_value = True  # true: 資料正確, 註冊成功
    if userID == "":
        return_value = False  # false: 資料不完全 註冊失敗

    s = Session()
    s.query(User).filter(User.emp_id == userID).update({'isRemoved': False})
    s.commit()
    s.close()

    return jsonify({
        'status': return_value,
    })


# update reagent's 'isRemoved'
@deleteTable.route("/removeReagent", methods=['POST'])
def remove_reagent():
    print("removeReagent....")
    request_data = request.get_json()
    reagentID = request_data['ID']

    return_value = True  # true: 資料正確, 註冊成功
    if reagentID == "":
        return_value = False  # false: 資料不完全 註冊失敗

    s = Session()
    s.query(Reagent).filter(Reagent.reag_id ==
                            reagentID).update({'isRemoved': False})
    s.commit()
    s.close()

    return jsonify({
        'status': return_value,
    })


# update supplier's 'isRemoved'
@deleteTable.route("/removeSupplier", methods=['POST'])
def remove_supplier():
    print("removeSupplier....")
    request_data = request.get_json()
    supplierID = request_data['ID']

    return_value = True  # true: 資料正確, 註冊成功
    if supplierID == "":
        return_value = False  # false: 資料不完全 註冊失敗

    if return_value:
        s = Session()
        s.query(Supplier).filter(Supplier.super_id ==
                                 supplierID).update({'isRemoved': False})
        s.commit()
        s.close()

    return jsonify({
        'status': return_value,
    })


# update product's 'isRemoved'
@deleteTable.route("/removeProduct", methods=['POST'])
def remove_product():
    print("removeProduct....")
    request_data = request.get_json()
    productID = request_data['ID']

    return_value = True  # true: 資料正確, 註冊成功
    if productID == "":
        return_value = False  # false: 資料不完全 註冊失敗

    if return_value:
        s = Session()
        s.query(Product).filter(Product.id ==
                                productID).update({'isRemoved': False})
        s.commit()
        s.close()

    return jsonify({
        'status': return_value,
    })


# update department' 'isRemoved'
@deleteTable.route("/removeDepartment", methods=['POST'])
def remove_department():
    print("removeDepartment....")
    request_data = request.get_json()
    departmentID = request_data['ID']

    return_value = True  # true: 資料正確, 註冊成功
    if departmentID == "":
        return_value = False  # false: 資料不完全 註冊失敗

    if return_value:
        s = Session()
        s.query(Department).filter(Department.id ==
                                departmentID).update({'isRemoved': False})
        s.commit()
        s.close()

    return jsonify({
        'status': return_value,
    })


# remove grid item's link
@deleteTable.route("/removeGrid", methods=['POST'])
def remove_grid():
    print("removeGrid....")
    request_data = request.get_json()
    reagentID = request_data['ID']
    gridID = request_data['GRID']

    return_value = True  # true: 資料正確, 註冊成功
    if reagentID == "" or gridID == "":
        return_value = False  # false: 資料不完全 註冊失敗

    s = Session()
    reagent = s.query(Reagent).filter_by(reag_id=reagentID).first()
    grid = s.query(Grid).filter_by(id=gridID).first()
    grid._reagents_on_grid.remove(reagent)

    s.commit()
    s.close()

    return jsonify({
        'status': return_value,
    })


# delete outtag item and update intag's stockOut_temp_count
@deleteTable.route("/deleteStockOutAndStockInData", methods=['POST'])
def delete_StockOut_and_StockIn_data():
    print("deleteStockOutAndStockInData....")
    request_data = request.get_json()

    _data = request_data['stockOut_array']
    _count = request_data['stockOut_count']
    print("_data, _count: ", _data, _count)

    return_value = True  # true: 資料正確
    if not _data or len(_data) != _count:
        return_value = False  # false: 資料不完全

    s = Session()
    outtag = s.query(OutTag).filter_by(id=_data['stockOutTag_ID']).first()
    s.delete(outtag)

    intag = s.query(InTag).filter_by(id=_data['stockOutTag_InID']).first()

    cursor = s.query(func.sum(OutTag.count)).filter(
        OutTag.intag_id == _data['stockOutTag_InID']).filter(
        OutTag.isRemoved == True)
    total = cursor.scalar()

    intag.stockOut_temp_count = total  # 修改入庫資料

    s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })
