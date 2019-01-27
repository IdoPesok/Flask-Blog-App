# Flask Blog App
Flask blog application where users can post their ideas and thoughts!

# Getting Started
Start off by cloning the repo and changing directories into the project directory.
<br/>
<br/>
Next you want to setup the database. To do so, enter a python enviornment and type...
```python
from blogapp import db
from blogapp.models import User, Post, Comment

db.create_all()
```
Finally you can go back into terminal and execute the run.py file

# Features
- Fully functional authentication system (login / register)
- Ability to recover forgotten password using flask_mail and secret tokens
- Custom CSS design
- Ability to update account/profile information at any time while logged in
- Profile Pictures
- Post any blog post you can think of
- Comment on any blog post
- Delete or edit any blog post
- Delete or edit any comment
