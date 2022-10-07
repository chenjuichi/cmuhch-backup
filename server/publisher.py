# 發布者（publisher）指令稿 publisher1.py
import paho.mqtt.client as mqtt

# 建立 MQTT Client 物件
client = mqtt.Client()

# 設定登入帳號密碼（若無則可省略）
# client.username_pw_set("myuser","mypassword")

# 連線至 MQTT 伺服器（伺服器位址,連接埠）
client.connect("127.0.0.1", 1883)

# 發布訊息至 hello/world 主題
client.publish("Station1/Layout1/Led1", "off")
