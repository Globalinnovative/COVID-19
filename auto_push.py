# -*- coding: utf-8 -*-
"""
Spyder Editor

Automatically update graph and make a pull request to the repository
"""

import covid19
import os
from datetime import datetime
from git import Repo

REPO_PATH = os.path.join(os.path.dirname(__file__))
README_PATH = os.path.join(REPO_PATH, 'README.md')
DATETIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Make the graph
covid19.main()

# Edit the README
with open(README_PATH, mode = 'r+', encoding = 'utf-8') as file:
    README_BACKUP = content = file.read()
    file.seek(0)
    file.write(content.replace('$date', DATETIME))
    file.truncate()

# GitPython
try:
    repo = Repo(REPO_PATH)
    repo.git.add('--all')
    repo.git.commit('-m', 'Update {}'.format(DATETIME))
    origin = repo.remote(name='origin')
    origin.push()
except Exception as err:
    print('Some error occured while pushing the code: {}'.format(err))
finally:
    print('GitPython successful')

# Restore the README
with open(README_PATH, mode = 'w', encoding = 'utf-8') as file:
    file.write(README_BACKUP)
