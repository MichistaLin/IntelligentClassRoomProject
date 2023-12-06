import serial
import serial.tools.list_ports
from datetime import datetime
import time
import multiprocessing
import os
from app.models import *
from flask import current_app
from threading import Thread

# 新建互斥信号量
mutex = multiprocessing.Lock()


# 连接端口
def connect_arduino(baudrate=9600, port=None, retries=5):
	"""
	:param baudrate: 波特率
	:param port: 端口号，类型为string
	:param retries: 重试次数
	:return: ser->端口对象
	"""
	if port is None:
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino" in p.description:
				port = p.device
				break
	if port is None:
		raise RuntimeError("Failed to find Arduino port automatically")

	print(f"Connecting to Arduino on {port}...")
	for attempt in range(retries):
		try:
			ser = serial.Serial(port, baudrate=baudrate, timeout=1)
			break
		except serial.SerialException as e:
			if attempt >= retries - 1:
				raise
			else:
				print(f"Could not connect to {port}, retrying...")
				time.sleep(1)
	else:
		raise RuntimeError(f"Failed to connect to {port} after {retries} retries")

	print(f"Connected to Arduino on port {port} successfully！")
	return ser


# 向arduino端口发送命令，返回值为下位机返回的数据或控制命令是否生效的结果
def send_cmd(ser, cmd, retries=3):
	"""
	:param ser: 端口对象
	:param cmd: 控制命令，类型string
	:param retries: 重试次数
	:return: 数据或结果，类型string
	"""
	for _ in range(retries):
		try:
			ser.write(cmd.encode())
			ser.flush()
			time.sleep(0.1)

			# TODO:按下位机返回值判断返回值是否正确
			echo = ser.readline().decode().strip()
			print(echo)
			# print(cmd)
			return echo
		except Exception as e:
			print(f"Error sending command: {e}")
			time.sleep(1)
	raise RuntimeError(f"Failed to send command {cmd} after {retries} retries")


# 从端口读取数据
def read_arduino(ser):
	"""
	:param ser:端口对象
	:return:data->string
	"""
	data = send_cmd(ser, "query env")

	return data


# 每隔2秒读取一次数据，用于前端展示实时状况
def read_arduino_periodic(app, connector, port="COM2"):
	"""
	:param connector: 传入连接端口的函数名，也就是connect_arduino（不要带括号），用于在子线程连接端口
	:param port: 端口号，类型string
	:return:
	"""
	with app.app_context():
		while True:
			try:
				mutex.acquire() # 加锁
				ser = connector(port=port)
				data = read_arduino(ser).split(",")[1:]
				print(data)
				ser.close()
				mutex.release()  # 解锁
				# TODO: 计算得到的数据并写入数据库
				if len(data) == 0:
					continue
				# 1. 温度
				temp = Temp(temperature=float(data[0]), date=datetime.now())
				db.session.add(temp)
				db.session.commit()
				# 2. 湿度
				humid = Humid(humidity=float(data[1]), date=datetime.now())
				db.session.add(humid)
				db.session.commit()
				# 3. 气压
				airp = Airp(air_pressure=float(data[2]) / 100000, date=datetime.now())
				db.session.add(airp)
				db.session.commit()
				# 4. 光照
				if data[3] == '':
					data[3] = '0'
				light = Light(light=(float(data[3])-250) / 5, date=datetime.now())
				db.session.add(light)
				db.session.commit()

			except Exception as e:
				print(e)
			time.sleep(2)


def start_arduino_reader(ser, port="COM2"):
	Thread(target=read_arduino_periodic, args=(current_app._get_current_object(), ser, port)).start()


if __name__ == '__main__':
	ser = connect_arduino(port="COM2")
	print("主线程ID：", os.getpid())
	# print(read_arduino(ser))
	send_cmd(ser, "hello world")
	ser.close()

	start_arduino_reader(connect_arduino, port="COM2")
	while True:
		if not reader.is_alive():
			print("Reader process exited, restarting...")
			reader = start_arduino_reader(connect_arduino, port="COM2")
		time.sleep(1)
