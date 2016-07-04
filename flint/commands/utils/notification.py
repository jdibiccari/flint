import click
import os

PROJECT = {
	'success': 'Added {project} project with target of ${target:.2f}',
	'project_nonunique': 'ERROR: A project by that name already exists.',
}
BACK = {
	'success': '{backer} backed project {project} for ${amount:.2f}',
	'project_not_found': 'ERROR: That project doesn\'t exist yet!',
	'backer_nonunique': 'ERROR: That backer has already backed this project!',
	'card_nonunique': 'ERROR: That card has already been added by another user!'
}
BACKER = {
	'not_found': '{backer} hasn\'t backed any projects.',
	'pledge': '-- Backed {project} for ${amount:.2f}'
}
LIST = {
	'pledge': '-- {backer} backed for ${amount:.2f}',
	'not_found': 'There\'s no project by the name {project}.',
	'target_reached': '{project} is successful!',
	'target_not_reached': '{project} needs ${to_goal:.2f} more to be successful!',
	'not_found': 'There\'s no project named {project}.'
}
VALIDATION ={
	'invalid_card': 'ERROR: This card is invalid',
	'invalid_amount': 'ERROR: Currency amounts must not be negative',
	'invalid_name': 'ERROR: {name} is not a valid name.'
}

def warn(msg):
	return click.secho(msg, fg='red')

def notify(msg):
	return click.secho(msg, fg='green')

def log(file, msg):
	import logging
	file = os.path.basename(file)
	logging.error('\n {}: {}'.format(file, msg))

def get_message(cmd_msgs, outcome, replace_with={}):
	if replace_with:
		return cmd_msgs[outcome].format(**replace_with)
	return cmd_msgs[outcome]
