import os
import json

path = os.path.dirname(__file__)

if 'ACTIVE_ENV' in os.environ and os.environ['ACTIVE_ENV'] == 'PRODUCTION':
	print('PRODUCTION')
	config = path + '/configProd.json'
elif 'ACTIVE_ENV' in os.environ and os.environ['ACTIVE_ENV'] == 'STAGING':
	print('STAGING')
	config = path + '/configStag.json'
else:
	print('DEVELOPMENT')
	config = path + '/configDev.json'

with open(config, 'r') as outfile:
	configuration = json.load(outfile)
