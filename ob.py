# -*- coding:utf-8 -*-

# lol使用国服客户端ob韩服

import sys
import os

# 搜索ob参数字符串
obParamsFeatures = '@start'

# 客户端路径
clientPath = r'D:\Game\英雄联盟\Game'

# 处理命令行参数
def handleParams():
	if len(sys.argv) == 1:
		print('error: please input obfile path')
		sys.exit(0)
	elif len(sys.argv) != 2:
		print('error: params error')
		sys.exit(0)
	else:
		print('success: file name: ' + sys.argv[1])
		return sys.argv[1]

# 提取观战参数
# obfile ob路径
def handleOBParams(obfile):
	with open(obfile) as f:
		for line in f:
			if line.find(obParamsFeatures) != -1:
				print('success: obparams: ' + line)
				return line
	print('error: can not extract ob params, please check your file')
	sys.exit(0)

# 开启客户端观战
def openClient(obparams):
	os.chdir(clientPath)
	os.system(obparams)

if __name__ == '__main__':
	obfile = handleParams()
	obparams = handleOBParams(obfile)
	print('success: open client')
	openClient(obparams)
