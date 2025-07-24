import os

env = os.getenv('SMARTDOC_ENV', 'dev')  # Default to dev

if env == 'prod':
    from .prod import *
elif env == 'uat':
    from .uat import *
else:
    from .dev import *
