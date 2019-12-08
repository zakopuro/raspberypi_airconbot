from slackbot.bot import listen_to
import re
import subprocess
import Adafruit_DHT
import time

@listen_to('室温')
@listen_to('温度')
@listen_to('湿度')
@listen_to('気温')
def return_temperature(message,*something):
    pin = 22
    # たまに前回の電圧情報？が残っているので2回計測
    humidity,temperature = Adafruit_DHT.read_retury(Adafruit_DHT.DHT22,pin)
    time.sleep(0.5)
    humidity,temperature = Adafruit_DHT.read_retury(Adafruit_DHT.DHT22,pin)
    if (humidity >= 80) & (temperature >= 30):
        comment = '蒸し暑いですね'
    elif (humidity <= 30) & (temperature <= 15):
        comment = '肌寒く、乾燥してます'
    else:
        comment = '快適かも？'
    message.reply('\n温度：{}℃,\n室温：{}%\n{}'.format(round(tempurature,1),round(humidity,1),comment))

@listen_to('暖房')
@listen_to('あたたかく')
@listen_to('だん')
def run_hot(message,*something):
    user_ID = message.channel._client.users[message.body['user']][u'name']
    message.reply('\n{}の命令で暖房をつけました。失敗してたらごめんね。'.format((user_ID)))
    subprocess.call('python3 irrp.py -p -g23 -f codes hot:on',shell=True)
    time.sleep((0.5))
    # 念の為2回実行
    subprocess.call('python3 irrp.py -p -g23 -f codes hot:on',shell=True)

@listen_to('暖房')
@listen_to('れい')
def run_cool(message,*something):
    user_ID = message.channel._client.users[message.body['user']][u'name']
    message.reply('\n{}の命令で冷房をつけました。失敗してたらごめんね。'.format((user_ID)))
    subprocess.call('python3 irrp.py -p -g23 -f codes cool:on',shell=True)
    time.sleep((0.5))
    # 念の為2回実行
    subprocess.call('python3 irrp.py -p -g23 -f codes cool:on',shell=True)

@listen_to('停止')
@listen_to('ストップ')
def stop_aircon(message,*something):
    user_ID = message.channel._client.users[message.body['user']][u'name']
    message.reply('\n{}の命令でエアコンを停止しました。失敗してたらごめんね。'.format((user_ID)))
    subprocess.call('python3 irrp.py -p -g23 -f codes aircon:stop',shell=True)
    time.sleep((0.5))
    # 念の為2回実行
    subprocess.call('python3 irrp.py -p -g23 -f codes aircon:stop',shell=True)


@listen_to('℃')
@listen_to('度')
def setting_temperature(message,*something):
    m = message.body['text']
    try:
        temperature = int(m[:-1])
        comment = '{}度に設定しました。エアコンを付けてない場合は最初に冷房か暖房をつけてください。'.format(temperature)
    except ValueError:
        comment = '「{温度}度」または「{温度}℃」の形式で入力してください'

    if 18 <= temperature <= 30:
        subprocess.call('python3 irrp.py -p -g23 -f codes temp:{}'.format(temperature),shell=True)
        time.sleep(0.5)
        subprocess.call('python3 irrp.py -p -g23 -f codes temp:{}'.format(temperature),shell=True)
    else:
        comment = '18〜30度の間で設定してください。'
    massage.reply(comment)


@listen_to('風量')
def setting_air_flow(message,*something):
    m = message['text']
    air_flow = m[2:]
    if air_flow == '最大':
        air_flow = 4
    elif air_flow == '最小':
        air_flow = 1
    elif air_flow == '自動':
        air_flow = 99

    try:
        air_flow = int(air_flow)
        if air_flow == 99:
            comment = '風量を自動に設定しました。'
        else:
            if 1 <= air_flow <= 4:
                comment = '風量を{}に設定しました。'.format(air_flow)
                subprocess.call('python3 irrp.py -p -g23 -f codes air:{}'.format(air_flow),shell=True)
            else:
                comment = '1〜4の間で設定してください。'
    except ValueError:
        comment = '「風量 {数値}」で入力してください。'

    message.reply(comment)