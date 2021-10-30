def func(name, param):
	param = param.split(' ', 2)
	try:
		x = int(param[0])
		y = int(param[1])
	except (IndexError, ValueError):
		return False, 'Invalid params'

	return True, f'{x}^{y}={x**y}'

minetest.register_chatcommand('power', {
	'description': 'Print the value of x to the power of y',
	'params': '[x] [y]',
	'func': func,
})
