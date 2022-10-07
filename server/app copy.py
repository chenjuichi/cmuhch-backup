
from urllib.request import Request
from flask import Flask, jsonify, request, abort, redirect, url_for
from flask_cors import CORS

from flask_mqtt import Mqtt


#import paho.mqtt.client as mqtt

app = Flask(__name__)

host_ip = '192.168.32.178'
app.config['MQTT_BROKER_URL'] = host_ip
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'flask_mqtt'
#app.config['TEMPLATES_AUTO_RELOAD'] = True
#app.config['MQTT_REFRESH_TIME'] = 1.0
# Set this item when you need to verify username and password
app.config['MQTT_USERNAME'] = ''
# Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''
# app.config['MQTT_KEEPALIVE'] = 30  # Set KeepAlive time in seconds
# If your server supports TLS, set it True
app.config['MQTT_TLS_ENABLED'] = False

# 建立 MQTT Client 物件
#mqtt_client = Mqtt(app)
mqtt_client = Mqtt(app, connect_async=True)

#CORS(app, resources={r'/*': {'origins': '*'}})
CORS(app)


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
    # if level == MQTT_LOG_ERR:
    print('Error: {}'.format(buf))
    # pass


@app.route("/")
def helloWorld():
    return "Hello, cross-origin-world!"


@app.route("/mqtt/stationA", methods=['POST'])
def mqtt_stationA():
    request_data = request.get_json()
    print("hello /mqtt/stationA: " + request_data['topic'])

    # 發布訊息至 Layout/Led 主題
    mqtt_client.publish('HELLO', request_data['msg'])

    return jsonify({
        'status': 'stationA success',
    })


if __name__ == '__main__':
    #    app.run(host='0.0.0.0', port=2020, debug=True)
    app.run(host=host_ip, port=5050, debug=True)
