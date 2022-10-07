import socket

import json

# --------------------------

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mqtt import Mqtt

#from flask_restful import Api

# --------------------------

from ajax.getTable import getTable
from ajax.createTable import createTable
from ajax.updateTable import updateTable
from ajax.deleteTable import deleteTable

from ajax.listTable import listTable

from ajax.excelTable import excelTable

# --------------------------

app = Flask(__name__)  # 初始化Flask物件

#api = Api(app)

# --------------------------

hostName = socket.gethostname()
local_ip = socket.getaddrinfo(hostName, None)
host_ip_for_lan = local_ip[3][4][0]  # for 有線網卡
host_ip_for_wifi = local_ip[1][4][0]  # for 無線網卡
print("system Lan ip:" + host_ip_for_lan, ", and wifi ip:" + host_ip_for_wifi)

# --------------------------

# host_ip = '192.168.0.14'    # for home #//////2/2-
host_ip = '192.168.32.178'  # for zh  #//////2/2-
# host_ip = '192.168.43.117'  # for mobile  #//////2/2-
app.config['MQTT_BROKER_URL'] = host_ip
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'cmu_hch_mqtt'
#app.config['TEMPLATES_AUTO_RELOAD'] = True
#app.config['MQTT_REFRESH_TIME'] = 1.0
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
# app.config['MQTT_KEEPALIVE'] = 30       # Set KeepAlive time in seconds
# If your server supports TLS, set it True
app.config['MQTT_TLS_ENABLED'] = False


# 建立 MQTT Client 物件
mqtt_client = Mqtt(app, connect_async=True)

# --------------------------

app.register_blueprint(getTable)
app.register_blueprint(updateTable)
app.register_blueprint(deleteTable)
app.register_blueprint(createTable)

app.register_blueprint(listTable)

app.register_blueprint(excelTable)

# --------------------------

CORS(app, resources={r'/*': {'origins': '*'}})
# CORS(app)


# --------------------------


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )


@mqtt_client.on_connect()
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        # 每次連線之後，重新設定訂閱主題
        mqtt_client.subscribe("Layout1/Led5")
    else:
        print('Bad connection. Code:', rc)


@mqtt_client.on_log()
def handle_logging(client, userdata, level, buf):
    if level == 16:
        #print('MQTT_LOG_DEBUG: {}'.format(buf))
        pass  # MQTT_LOG_DEBUG
    else:
        print('Error: {}'.format(buf))
    # pass


# --------------------------


@app.route("/")
def helloWorld():
    return "Hello..."


@app.route("/mqtt/stationA", methods=['POST'])
def mqtt_stationA():
    request_data = request.get_json()
    print("hello /mqtt/stationA: " + request_data['topic'])
    print("message: " + request_data['layout'] + ' ' +
          request_data['led'] + ' ' + request_data['msg'])

    # 發布訊息至 Layout/Led 主題
    MQTT_MSG = json.dumps(
        {"Layout": request_data['layout'], "Led": request_data['led'], "Msg": request_data['msg']})
    mqtt_client.publish('Station1', MQTT_MSG)

    return jsonify({
        'status': 'stationA success',
    })


# --------------------------


if __name__ == '__main__':
    #    app.run(host='0.0.0.0', port=2020, debug=True)
    app.run(host=host_ip, port=5050, debug=True)
