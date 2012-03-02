Bottlepy User Authentication
======

About
----------------

This module provides basic methods to manage users authentication state on your site.
This module uses encripted bottle cookies to store user id from database and perform checks using this id.

Dependancies
------------

Just [Python 2.7+][py] and [Bottle][bottle].
You also need to have some database module. Every "self.db" method in this module is just a demo. 

Example
------------------------

``` python
from bottle import *
from bottle_user_auth import User

@root.route('/')
def index_page(): #displays index page
    user = User() #here and below - creates an instance of User class
    if user.loggedin:
        return 'You are an authenticated user'
    redirect('/login')

@root.post('/login')
@view('login_page')
def login_page():
    #assume you have a login page with two fields: 
    #"email" and "password" and submit button

@root.post('/login')
def user_login(): #getting credentials from POST request from login page
    user = User()

    if user.authenticate( 
            request.POST.get( 'email' ),
            request.POST.get( 'password' )
    ):
        redirect('/')

    redirect('/login/error')
```

  [py]: http://python.org/
  [bottle]: http://bottlepy.org/
