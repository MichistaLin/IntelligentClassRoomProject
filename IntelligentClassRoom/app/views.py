# views.py： 路由+视图函数

from flask import Blueprint, render_template, jsonify, request
import datetime
from .serialapi import connect_arduino, send_cmd
from .models import *


# 蓝图
blue = Blueprint('user',__name__)


@blue.route('/')
def index():
    return render_template('index.html')


@blue.route('/index/')
def index1():
    return render_template('pages/plugin-echarts.html')


@blue.route('/settings/')
def settings():
    return render_template('pages/settings.html')


# 查询并展示lcd灯的状态
@blue.route('/led/')
def led():
    # 1. 连接端口
    ser = connect_arduino(port="COM2")
    # 2. 发送命令
    res = send_cmd(ser, "query led").split(',')[1:5]
    # 3. 关闭端口
    ser.close()
    print(res)
    for i in range(len(res)):
        if res[i] == '1':
            res[i] = '开'
        else:
            res[i] = '关'
    return render_template('pages/led.html', res=res)


# 历史数据展示
@blue.route('/historydata/')
def historydata():
    return render_template('pages/historydata.html')


# 接口部分
# 展示首页图表数据
@blue.route('/getdata/', methods=['GET'])
def getdata():
    # 获取前端传递的参数
    total = int(request.args.get('total'))
    # 1. 查询温度，按照id降序排列
    temps = Temp.query.order_by(Temp.id.desc()).limit(int(total)).all()
    # 2. 查询湿度
    humids = Humid.query.order_by(Humid.id.desc()).limit(int(total)).all()
    # 3. 查询气压
    airps = Airp.query.order_by(Airp.id.desc()).limit(int(total)).all()
    # 4. 查询光照
    lights = Light.query.order_by(Light.id.desc()).limit(int(total)).all()
    # 5. 处理数据
    temps_data = []
    temps_date = []
    humids_data = []
    humids_date = []
    airps_data = []
    airps_date = []
    lights_data = []
    lights_date = []
    for temp, humid, airp, light in zip(temps, humids, airps, lights):
        temps_data.append(temp.temperature)
        temps_date.append(temp.date.strftime('%Y-%m-%d %H:%M:%S'))
        humids_data.append(humid.humidity)
        humids_date.append(humid.date.strftime('%Y-%m-%d %H:%M:%S'))
        airps_data.append(airp.air_pressure)
        airps_date.append(airp.date.strftime('%Y-%m-%d %H:%M:%S'))
        lights_data.append(light.light)
        lights_date.append(light.date.strftime('%Y-%m-%d %H:%M:%S'))
    # 5. 将数据转换为json格式
    data = {
        'temp':{'data':temps_data[::-1], 'date':temps_date[::-1]},
        'humid':{'data':humids_data[::-1], 'date':humids_date[::-1]},
        'airp':{'data':airps_data[::-1], 'date':airps_date[::-1]},
        'light':{'data':lights_data[::-1], 'date':lights_date[::-1]},
    }
    return jsonify(data)


# 展示传感器数据
@blue.route('/getsensor/', methods=['GET'])
def getsensor():
    # 查询数据库最新的一条数据
    # 1. 查询温度
    temp = Temp.query.order_by(Temp.id.desc()).first()
    # 2. 查询湿度
    humid = Humid.query.order_by(Humid.id.desc()).first()
    # 3. 查询气压
    airp = Airp.query.order_by(Airp.id.desc()).first()
    # 4. 查询光照
    light = Light.query.order_by(Light.id.desc()).first()
    # 5. 处理数据
    temp_data = temp.temperature
    temp_date = temp.date.strftime('%Y-%m-%d %H:%M:%S')
    humid_data = humid.humidity
    humid_date = humid.date.strftime('%Y-%m-%d %H:%M:%S')
    airp_data = airp.air_pressure
    airp_date = airp.date.strftime('%Y-%m-%d %H:%M:%S')
    light_data = light.light
    light_date = light.date.strftime('%Y-%m-%d %H:%M:%S')
    # 6. 将数据转换为json格式
    data = {
        'temp':{'data':temp_data, 'date':temp_date},
        'humid':{'data':humid_data, 'date':humid_date},
        'airp':{'data':airp_data, 'date':airp_date},
        'light':{'data':light_data, 'date':light_date},
    }
    return jsonify(data)


# 控制led状态
@blue.route('/controlled/', methods=['GET'])
def controlled():
    # 获取前端传递的参数
    lid = int(request.args.get('id')) - 1
    state = request.args.get('state')
    if lid < 4:
        cmd = "control led alone " + str(lid) + "," + str(state)
    else:
        if state == '1':
            cmd = "control led on"
        elif state == '0':
            cmd = "control led off"
        else:
            cmd = "control led track"
    # 1. 连接端口
    ser = connect_arduino(port="COM2")
    # 2. 发送命令
    res = send_cmd(ser, cmd)
    # 3. 关闭端口
    ser.close()
    print(res)
    return jsonify({'msg': res})


# 追踪模式下的led状态
@blue.route('/track/', methods=['GET'])
def track():
    # 1. 连接端口
    ser = connect_arduino(port="COM2")
    # 2. 发送命令
    res = send_cmd(ser, "query led").split(',')[1:5]
    # 3. 关闭端口
    ser.close()
    print(res)
    for i in range(len(res)):
        if res[i] == '1':
            res[i] = '开'
        else:
            res[i] = '关'
    return jsonify({'res': res})


# 初始化展示历史数据页
@blue.route('/inithistory/')
def inithistory():
    # 1. 查询今天的所有温度数据
    temps = Temp.query.filter(Temp.date.like(datetime.date.today().strftime('%Y-%m-%d') + '%')).all()
    # 2. 查询今天的所有湿度数据
    humids = Humid.query.filter(Humid.date.like(datetime.date.today().strftime('%Y-%m-%d') + '%')).all()
    # 3. 查询今天的所有气压数据
    airps = Airp.query.filter(Airp.date.like(datetime.date.today().strftime('%Y-%m-%d') + '%')).all()
    # 4. 查询今天的所有光照数据
    lights = Light.query.filter(Light.date.like(datetime.date.today().strftime('%Y-%m-%d') + '%')).all()
    # 5. 处理数据
    temps_data = []
    temps_date = []
    humids_data = []
    humids_date = []
    airps_data = []
    airps_date = []
    lights_data = []
    lights_date = []
    for temp, humid, airp, light in zip(temps, humids, airps, lights):
        temps_data.append(temp.temperature)
        temps_date.append(temp.date.strftime('%Y-%m-%d %H:%M:%S'))
        humids_data.append(humid.humidity)
        humids_date.append(humid.date.strftime('%Y-%m-%d %H:%M:%S'))
        airps_data.append(airp.air_pressure)
        airps_date.append(airp.date.strftime('%Y-%m-%d %H:%M:%S'))
        lights_data.append(light.light)
        lights_date.append(light.date.strftime('%Y-%m-%d %H:%M:%S'))
    # 6. 将数据转换为json格式
    data = {
        "temp": {"data": temps_data, "date": temps_date},
        "humid": {"data": humids_data, "date": humids_date},
        "airp": {"data": airps_data, "date": airps_date},
        "light": {"data": lights_data, "date": lights_date},
    }
    return jsonify(data)


# 历史数据展示
@blue.route('/gethistory/', methods=['GET'])
def gethistory():
    temps, humids, airps, lights = [], [], [], []
    # 获取前端传递的参数
    value = request.args.get('value') # 表示获取几天内的数据
    if value == '1':
        # 1. 查询今天的所有温度数据
        temps = Temp.query.filter(Temp.date.like(datetime.date.today().strftime('%Y-%m-%d') + '%')).all()
        # 2. 查询今天的所有湿度数据
        humids = Humid.query.filter(Humid.date.like(datetime.date.today().strftime('%Y-%m-%d') + '%')).all()
        # 3. 查询今天的所有气压数据
        airps = Airp.query.filter(Airp.date.like(datetime.date.today().strftime('%Y-%m-%d') + '%')).all()
        # 4. 查询今天的所有光照数据
        lights = Light.query.filter(Light.date.like(datetime.date.today().strftime('%Y-%m-%d') + '%')).all()
    elif value == '3':
        # 1. 查询3天内的所有温度数据
        temps = Temp.query.filter(Temp.date > ((datetime.date.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d') + '%')).all()
        # 2. 查询3天内的所有湿度数据
        humids = Humid.query.filter(Humid.date > ((datetime.date.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d') + '%')).all()
        # 3. 查询3天内的所有气压数据
        airps = Airp.query.filter(Airp.date > ((datetime.date.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d') + '%')).all()
        # 4. 查询3天内的所有光照数据
        lights = Light.query.filter(Light.date > ((datetime.date.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d') + '%')).all()
    elif value == '7':
        # 1. 查询7天内的所有温度数据
        temps = Temp.query.filter(Temp.date > ((datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d') + '%')).all()
        # 2. 查询7天内的所有湿度数据
        humids = Humid.query.filter(Humid.date > ((datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d') + '%')).all()
        # 3. 查询7天内的所有气压数据
        airps = Airp.query.filter(Airp.date > ((datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d') + '%')).all()
        # 4. 查询7天内的所有光照数据
        lights = Light.query.filter(Light.date > ((datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d') + '%')).all()
    # 处理数据
    temps_data = []
    temps_date = []
    humids_data = []
    humids_date = []
    airps_data = []
    airps_date = []
    lights_data = []
    lights_date = []
    for temp, humid, airp, light in zip(temps, humids, airps, lights):
        temps_data.append(temp.temperature)
        temps_date.append(temp.date.strftime('%Y-%m-%d %H:%M:%S'))
        humids_data.append(humid.humidity)
        humids_date.append(humid.date.strftime('%Y-%m-%d %H:%M:%S'))
        airps_data.append(airp.air_pressure)
        airps_date.append(airp.date.strftime('%Y-%m-%d %H:%M:%S'))
        lights_data.append(light.light)
        lights_date.append(light.date.strftime('%Y-%m-%d %H:%M:%S'))
    # 将数据转换为json格式
    data = {
        'temp':{'data':temps_data, 'date':temps_date},
        'humid':{'data':humids_data, 'date':humids_date},
        'airp':{'data':airps_data, 'date':airps_date},
        'light':{'data':lights_data, 'date':lights_date},
    }
    return jsonify(data)



