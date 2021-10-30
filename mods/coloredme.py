import random

def func(name, param):
	color = random.choice(['blue', 'red'])
	name = minetest.colorize(color, '* ' + name)
	minetest.chat_send_all(f'{name} {param}')

minetest.register_chatcommand('coloredme', {
	'description': 'Show chat action with colored player\'s name',
	'params': '[action]',
	'func': func,
})
