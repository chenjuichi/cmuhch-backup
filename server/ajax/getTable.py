from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from database.tables import User, Permission, Department, Setting, Supplier, Product, InTag, Session

from flask_cors import CORS

getTable = Blueprint('getTable', __name__)


# ------------------------------------------------------------------

'''
def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers",
                         "x-requested-with,content-type")
    response.headers.add("Access-Control-Allow-Methods", "POST")
    return response


@getTable.before_request
def oauth_verify(*args, **kwargs):
    """Ensure the oauth authorization header is set"""
    if request.method in ['OPTIONS', ]:
        return
    # if not _is_oauth_valid():
    #    return some_custome_error_response("you need oauth!")


@getTable.after_request
def af_request(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return resp
'''

'''
def props(cls):
    return [i for i in cls.__dict__.keys() if i[:1] != '_']
'''

# list user, department, permission and setting table all data by employee id and password


@getTable.route('/login', methods=['POST'])
def login():
    print("login....")
    request_data = request.get_json()
    userID = (request_data['empID'] or '')
    password = (request_data['password'] or '')
    # remember = True if request_data['remember'] else False

    s = Session()
    user = s.query(User).filter_by(emp_id=userID).first()
    print("login user: ", user)

    xx = not user.isRemoved  # isRemoved=False, 表示該使用者已被註記移除

    if not user or not check_password_hash(user.password, password) or xx:
        return_value = False  # if the user doesn't exist or password is wrong, reload the page
        _user_object = {}
    else:
        # if the above check passes, then we know the user has the right credentials
        return_value = True

        dep_item = s.query(Department).filter_by(id=user.dep_id).first()
        perm_item = s.query(Permission).filter_by(
            id=user.perm_id).first()
        setting_item = s.query(Setting).filter_by(id=user.setting_id).first()

        s.query(User).filter(User.emp_id == userID).update({'isOnline': True})
        s.commit()

        _user_object = {
            'empID': user.emp_id,
            'name': user.emp_name,
            'dep': dep_item.dep_name,
            'dep_id': dep_item.id,
            'perm_name': perm_item.auth_name,
            'perm': perm_item.auth_code,
            'password': password,
            'setting_items_per_page': setting_item.items_per_page,
            'setting_message': setting_item.message,
        }

    s.close()

    return jsonify({
        'status': return_value,
        'user': _user_object
    })


# list supplier and inTag table all data by select product object
@getTable.route("/listSuppliersBySelect", methods=['POST'])
def list_suppliers_by_select():
    print("listSuppliersBySelect....")

    request_data = request.get_json()
    selectedProducts = (request_data['catalogs'])
    print("product catalogs: ", selectedProducts)

    _results_for_supplier = []
    _results_for_stockOut = []

    s = Session()

    if selectedProducts:    # 有產品類別選項資料
        products = s.query(Product).all()
        for product in products:  # 列出產品類別
            if product.name in selectedProducts:
                #print("*: ", product.name)
                for supplier in product._suppliers:  # 列出供應商
                    #print("--> ", supplier.super_name)
                    _results_for_supplier.append(supplier.super_name)

                    for reagent in supplier._reagents:  # 列出該供應商的所有試劑編號
                        #print("b reagent: ", reagent.id)
                        _inTag = s.query(InTag).filter_by(
                            reagent_id=reagent.id).first()
                        if _inTag:
                            temp = _inTag.count - _inTag.stockOut_temp_count
                        if _inTag and temp > 0 and _inTag.isRemoved:    # 列出在庫所有試劑資料
                            #print("a reagent: ", _inTag.reagent_id)
                            _obj = {
                                'stockIn_reagent_id': reagent.reag_id,
                                'stockIn_reagent_name': reagent.reag_name,
                                'stockIn_supplier': supplier.super_name,
                                'stockIn_reagent_period': reagent.reag_period,
                                'stockIn_date': _inTag.intag_date,  # 入庫日期
                                'stockIn_reagent_Out_unit': reagent.reag_Out_unit,
                                # 'stockIn_reagent_Out_cnt': _inTag.count,
                                'stockIn_reagent_Out_cnt': temp,
                                # 'stockIn_reagent_Out_cnt': 1,
                                'stockIn_id': _inTag.id,
                            }
                            _results_for_stockOut.append(_obj)

    s.close()

    return jsonify({
        'status': 'success',
        'outputs_for_supplier': _results_for_supplier,
        'outputs_for_stockOut': _results_for_stockOut,
    })


# list StockIn table all data by select supplier
@getTable.route("/listStockInDataBySelect", methods=['POST'])
def list_stockInData_by_Select():
    print("listStockInDataBySelect....")

    request_data = request.get_json()
    selectedSuppliers = (request_data['suppliers'])
    selectedCatalogs = (request_data['catalogs'])
    print("product suppliers: ", selectedSuppliers)
    print("product catalogs: ", selectedCatalogs)

    _results_for_stockOut = []

    s = Session()
# ===狀況1
    if selectedCatalogs and selectedSuppliers:  # 有產品類別和供應商選項資料
        products = s.query(Product).all()
        for product in products:  # 列出產品類別
            if product.name in selectedCatalogs:  # 選項資料內有該筆產品類別名稱
                #print("*: ", product.name)
                for supplier in product._suppliers:  # 列出供應商
                    if supplier.super_name in selectedSuppliers:  # 選項資料內有該筆供應商名稱
                        #print("--> ", supplier.super_name)
                        for reagent in supplier._reagents:  # 列出試劑
                            _inTag = s.query(InTag).filter_by(
                                reagent_id=reagent.id).first()
                            if _inTag:
                                temp = _inTag.count - _inTag.stockOut_temp_count
                            if _inTag and temp > 0 and _inTag.isRemoved:    # 列出在庫所有試劑資料
                                _obj = {
                                    'stockIn_reagent_id': reagent.reag_id,
                                    'stockIn_reagent_name': reagent.reag_name,
                                    'stockIn_supplier': supplier.super_name,
                                    'stockIn_reagent_period': reagent.reag_period,
                                    'stockIn_date': _inTag.intag_date,  # 入庫日期
                                    'stockIn_reagent_Out_unit': reagent.reag_Out_unit,
                                    # 'stockIn_reagent_Out_cnt': _inTag.count,
                                    'stockIn_reagent_Out_cnt': temp,
                                    # 'stockIn_reagent_Out_cnt': 1,
                                    'stockIn_id': _inTag.id,
                                }
                                _results_for_stockOut.append(_obj)
# ===狀況2
    elif not selectedCatalogs and selectedSuppliers:  # 只有供應商選項資料
        suppliers = s.query(Supplier).all()

        for supplier in suppliers:  # 列出供應商
            if supplier.super_name in selectedSuppliers:  # 選項資料內有該筆供應商名稱
                #print("*: ", supplier.super_name)

                for reagent in supplier._reagents:  # 列出該供應商的所有試劑編號
                    #print("b reagent: ", reagent.id)

                    _inTag = s.query(InTag).filter_by(
                        reagent_id=reagent.id).first()
                    if _inTag:
                        temp = _inTag.count - _inTag.stockOut_temp_count
                    if _inTag and temp > 0 and _inTag.isRemoved:    # 列出在庫所有試劑資料
                        _obj = {
                            'stockIn_reagent_id': reagent.reag_id,
                            'stockIn_reagent_name': reagent.reag_name,
                            'stockIn_supplier': supplier.super_name,
                            'stockIn_reagent_period': reagent.reag_period,
                            'stockIn_date': _inTag.intag_date,  # 入庫日期
                            'stockIn_reagent_Out_unit': reagent.reag_Out_unit,
                            # 'stockIn_reagent_Out_cnt': _inTag.count,
                            'stockIn_reagent_Out_cnt': temp,
                            # 'stockIn_reagent_Out_cnt': 1,
                            'stockIn_id': _inTag.id,
                        }
                        _results_for_stockOut.append(_obj)
# ===狀況3
    elif selectedCatalogs and not selectedSuppliers:  # 只有產品類別選項資料
        products = s.query(Product).all()
        for product in products:  # 列出產品類別
            if product.name in selectedCatalogs:  # 選項資料內有該筆產品類別名稱
                for supplier in product._suppliers:  # 列出供應商
                    # if supplier.super_name in selectedSuppliers:  # 選項資料內有該筆供應商名稱
                    for reagent in supplier._reagents:  # 列出試劑
                        _inTag = s.query(InTag).filter_by(
                            reagent_id=reagent.id).first()
                        print("_inTag: ", _inTag)
                        if _inTag:
                            temp = _inTag.count - _inTag.stockOut_temp_count
                        if _inTag and temp > 0 and _inTag.isRemoved:    # 列出在庫所有試劑資料
                            _obj = {
                                'stockIn_reagent_id': reagent.reag_id,
                                'stockIn_reagent_name': reagent.reag_name,
                                'stockIn_supplier': supplier.super_name,
                                # 'stockIn_supplier': '',
                                'stockIn_reagent_period': reagent.reag_period,
                                'stockIn_date': _inTag.intag_date,  # 入庫日期
                                'stockIn_reagent_Out_unit': reagent.reag_Out_unit,
                                # 'stockIn_reagent_Out_cnt': _inTag.count,
                                'stockIn_reagent_Out_cnt': temp,
                                # 'stockIn_reagent_Out_cnt': 1,
                                'stockIn_id': _inTag.id,
                            }
                            _results_for_stockOut.append(_obj)

    s.close()

    return jsonify({
        'status': 'success',
        # 'outputs_for_supplier': _results_for_supplier,
        'outputs_for_stockOut': _results_for_stockOut,
    })
