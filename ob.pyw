# -*- coding:utf-8 -*-

"""lol使用国服客户端ob韩服
"""

import sys
import os
import ctypes
import configparser
from tkinter import *
import tkinter.filedialog


class Application(Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.pack()
		self.cf = configparser.ConfigParser()
		try:
			self.cf.read('ob.conf')
			self.lol_client_path = self.cf.get('settings', 'client')
			self.ob_file_path = self.cf.get('settings', 'ob_file')
		except:
			self.lol_client_path = self.ob_file_path = ''
			self.cf.add_section('settings')
			self.cf.set('settings', 'client', '')
			self.cf.set('settings', 'ob_file', '')
			with open('ob.conf', 'w') as f:
				self.cf.write(f)
		
		self.create_widgets()
	
	def create_widgets(self):
		"""创建控件
		"""
		self.lol_client_path_label = Label(self, text='请设置League of Legends.exe位置(一般在游戏目录/Game/下)' if self.lol_client_path == '' else self.lol_client_path)
		self.ob_file_path_label = Label(self, text='请选择ob文件位置' if self.ob_file_path == '' else self.ob_file_path)
		self.choose_lol_client_path_btn = Button(self, text='...', command=self.choose_lol_client_file)
		self.choose_ob_file_path_btn = Button(self, text='...', command=self.choose_ob_file)
		self.start_ob_btn = Button(self, text='开始观战', command=self.start_ob)
		
		self.lol_client_path_label.pack()
		self.choose_lol_client_path_btn.pack()
		self.ob_file_path_label.pack()
		self.choose_ob_file_path_btn.pack()
		self.start_ob_btn.pack()
	
	def choose_lol_client_file(self):
		"""选择客户端路径
		"""
		self.lol_client_path = tkinter.filedialog.askopenfilename()
		self.lol_client_path_label.config(text=self.lol_client_path)
		
		# 更新配置文件
		self.cf.set('settings', 'client', self.lol_client_path)
		with open('ob.conf', 'w') as f:
			self.cf.write(f)

	def choose_ob_file(self):
		"""选择ob文件路径
		"""
		self.ob_file_path = tkinter.filedialog.askopenfilename()
		self.ob_file_path_label.config(text=self.ob_file_path)
		
		# 更新配置文件
		self.cf.set('settings', 'ob_file', self.ob_file_path)
		with open('ob.conf', 'w') as f:
			self.cf.write(f)

	def start_ob(self):
		"""开启观战
		"""
		# 搜索ob参数字符串
		ob_param = '@start'
		with open(self.ob_file_path, 'r', encoding='UTF-8') as f:
			for line in f:
				if line.find(ob_param) != -1:
					ob_param = line
		
		# 写入临时bat中
		with open(os.path.join(os.path.dirname(self.lol_client_path), 'tmp.bat'), 'w') as f:
			f.write(ob_param.strip())
			
		# 切换目录
		os.chdir(os.path.dirname(self.lol_client_path))
		
		# 请求管理员权限
		try:
			if ctypes.windll.shell32.IsUserAnAdmin():
				# 观战
				os.system('tmp.bat')
			else:
				if sys.version_info[0] == 3:
					ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, None, None, 1)
					# 观战
					os.system('tmp.bat')
				else:#in python2.x
					ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
		except:
			print('???')
		

if __name__ == '__main__':
	root = Tk()
	app = Application(master=root)
	app.mainloop()
