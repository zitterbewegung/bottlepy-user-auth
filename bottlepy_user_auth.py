# -*- coding: UTF-8 -*-

# THIRD-PARTY MODULES
from bottle import request, response
import time

#LOCAL MODULES
import database
#Here you can import your database module, this is a demo import

class User:

    def __init__( self ):
        self.db = database.Database() #database connection
        self.COOKIE_SECRET_KEY = 'my_very_secret_key' #change this key to yours
        self.loggedin = False
        self.credentials = None
        self.validate() #validating user to see if he is logged in
    
    def authenticate( self , email , password ):
    
        '''
            @type email str
            @type password dict
            
            Checks user credentials and authenticates him in system.
        '''
        
        if email and password:
            user = self.db.find_user( email, password ) #if user exitsts

            if user:
                last_login = {
                    'last_login': time.strftime( 
                                        '%Y.%m.%d %H:%M:%S GMT',
                                        time.gmtime( time.time() )
                                    )
                }
                self.db.update_user( email , last_login ) #updating last_login
                self.set_cookie( user['user_id'] )
                self.loggedin = True
                self.credentials = user
                return True
                
        return False
        
    def logout( self ):
    
        '''
            Initiates user logout by destoying cookie.
        '''
        
        self.remove_cookie()
        self.loggedin = False
        self.credentials = None

        return True
        
    def register( self , email , password ):
    
        '''
            @type email str
            @type password str
            @type accepted str
            
            Get email, password and age acceptance from register page, 
            checks if email is already registered, hashes password with 
            md5 and store user data.
        '''
        
        if email and password:

            if not self.db.find_user( email ): #no user exists
                uid = self.db.add_user( email , password )

                if uid: #if user added successful
                    self.set_cookie( uid )
                    self.loggedin = True
                    self.credentials = self.db.return_user_by_objectid( uid )
                    return True

        return False    

    def validate( self ):
    
        '''
            Validates user email credential by decrypting encrypted cookie.
            Indicates that user is logged in and verified. If verification
            fails - destroys cookie by calling logout method ( because of
            possible cookie fraud ). Stores user info in credentials
            attribute in case of successful decryption.
        '''
        
        uid = request.get_cookie( '__utmb' , secret = self.COOKIE_SECRET_KEY )
        user = self.db.return_user_by_objectid( uid )

        if user:
            self.loggedin = True
            self.credentials = user
            return True
            
        self.logout()
        return None
        
    #COOKIES
        
    def set_cookie( self, uid ):
        
        '''
            Sets user cookie based on his uid.
        '''
            
        response.set_cookie( 
                '__utmb',
                uid,
                secret = self.COOKIE_SECRET_KEY,
                expires = time.time() + ( 3600*24*365 ),
                domain = '.python.rodriges.org',
                path = '/'
        )
        
    def remove_cookie( self ):
    
        '''
            Destroys user cookie.
        '''
        
        response.set_cookie(
                '__utmb',
                '',
                secret = self.COOKIE_SECRET_KEY,
                expires = time.time() - ( 3600*24*365 ),
                domain = '.python.rodriges.org',
                path = '/'
        )