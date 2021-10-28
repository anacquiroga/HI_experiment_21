from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=0, participation_fee=10)
SESSION_CONFIGS = [dict(name='exp_test', num_demo_participants=1, app_sequence=['HI_experiment', 'Survey'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'CHF'
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['color', 'q_order', 'expiry', 'stimuli']
SESSION_FIELDS = []
ROOMS = [dict(name='complab', display_name='Computer Lab', participant_label_file='_rooms/complab.txt')]


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


