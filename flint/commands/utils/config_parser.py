import os
import sys
from ConfigParser import SafeConfigParser

def parse(section, option, config_file=None):
	if not config_file:
		config_file = 'flint_config.ini'
	parser = SafeConfigParser()
	parser.read(config_file)
	return parser.get(section, option)