import PySimpleGUI as sg
import json
from sys import exit

FONT_SETTING = ('Arial', 15)
sg.theme('Black')

items_list = [
		]

prio_items = [
]

def save_items(items, priority):
	with open('stock_info.json', 'w') as file:
		json.dump([items, priority], file)
def load_items():
	try:
		with open('stock_info.json', 'r') as file:
			load = json.load(file)	
			items = load[0]
			prio = load[1]
			return items, prio 
	except FileNotFoundError:
		pass
	except json.decoder.JSONDecodeError:
		clicked = sg.popup_yes_no('Could not read stock_info.json. The file may be damaged or corrupted. Continue and overwrite stock_info.json?', font=FONT_SETTING)
		if clicked == 'No':
			exit()
		else:
			return [], []




items_list, prio_items = load_items()

entry_box = [	[sg.Input(size=15, key='NEW_ITEM')],
				[sg.Text('Amount'), sg.Input(size=5, key='QUANTITY_IN')],
				[sg.Button('Add'), sg.Button('Remove')]]

layout = [	
			[sg.Table(values=items_list, headings=['ITEM','#'], key='TAB', col_widths=[15,4], auto_size_columns=False, enable_events=True), sg.Frame('', entry_box, relief='flat')]
				]

window = sg.Window("Title", layout, font=FONT_SETTING)

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break

	if event == 'TAB':
		index = values[event][0]
		print(items_list[index])

	if event == 'Add':
		if values['NEW_ITEM'] != '' and values['QUANTITY_IN'].isnumeric():
			if values['NEW_ITEM'] in [x[0] for x in items_list]:
				index = [x[0] for x in items_list].index(values['NEW_ITEM'])
				items_list[index][1] += int(values['QUANTITY_IN'])
				window['TAB'].update(items_list)
			else:
				items_list.append([values['NEW_ITEM'], int(values['QUANTITY_IN'])])
				window['TAB'].update(items_list)
			save_items(items_list, prio_items)

	if 	event == 'Remove':
		if values['NEW_ITEM'] != '' and values['QUANTITY_IN'].isnumeric():
			if values['NEW_ITEM'] in [x[0] for x in items_list]:
				index = [x[0] for x in items_list].index(values['NEW_ITEM'])
				if int(values['QUANTITY_IN']) > items_list[index][1]:
					sg.popup("Quantity to remove is greater than the quantity in stock!", title='Error', font=FONT_SETTING)
				else:
					items_list[index][1] -= int(values['QUANTITY_IN'])
					window['TAB'].update(items_list)



window.close()