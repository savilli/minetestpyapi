#!/usr/bin/python3
import json
import os

functions = []

def api_write(r):
	mod_api_mtos.write(json.dumps(r))
	mod_api_mtos.write('\n')
	mod_api_mtos.flush()

class LuaFunctionWrapper():
	def __init__(self, module_name, name):
		self.module_name = module_name
		self.name = name
	
	def __call__(self, *args):
		api_write({'_lua_function': self.name, '_lua_module': self.module_name, 'args': pack_args(args)})
		return get_results()

class LuaModuleWrapper():
	def __init__(self, name):
		self.name = name

	def __getattr__(self, item):
		return LuaFunctionWrapper(self.name, item)

def pack_args(args):
	if type(args) == tuple:
		args = list(args)

	if callable(args):
		functions.append(args)
		args = {'_function': len(functions) - 1}
	elif type(args) == dict:
		for k, v in args.items():
			args[k] = pack_args(v)
	elif type(args) == list:
		for k, v in enumerate(args):
			args[k] = pack_args(v)

	return args

def get_results():
	while True:
		line = mod_api_stom.readline()
		if not line:
			return

		r = json.loads(line)
		if type(r) == dict and '_function' in r:
			ret = functions[r['_function']](*r['args'])
			if type(ret) != tuple:
				ret = [ret]
			api_write(pack_args(ret))
		else:
			return r

def serve():
	__builtins__.minetest = LuaModuleWrapper('minetest')

	for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'mods')):
		if filename.endswith('.py'):
			__import__(f'mods.{filename[:-3]}')

	api_write(True)
	assert(get_results() == None)

def cleanup():
	try:
		os.remove("mod_api_stom")
	except FileNotFoundError:
		pass
	try:
		os.remove("mod_api_mtos")
	except FileNotFoundError:
		pass

def main():
	global mod_api_stom, mod_api_mtos

	cleanup()
	os.mkfifo("mod_api_stom", 0o600)
	os.mkfifo("mod_api_mtos", 0o600)

	try:
		mod_api_stom = open("mod_api_stom", "r")
		mod_api_mtos = open("mod_api_mtos", "w")
		serve()
	finally:
		mod_api_stom.close()
		mod_api_mtos.close()
		cleanup()

if __name__ == '__main__':
	main()
