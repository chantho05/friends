from __future__ import unicode_literals

from django.db import models
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
# from django.contrib.auth.models import User



# Create your models here.
class UserManager(models.Manager):

    def register_valdiation(self, postData):
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        errors = []
        if len(postData['name']) < 2:
            errors.append("Your name is too short")
        if len(postData['user_name']) < 2:
            errors.append("Your username is too short")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("You must submit a valid email")
        if postData['password'] != postData['c_password']:
            errors.append("Your passwords do not match")
        try:
            if datetime.strptime(postData["birthday"], '%Y-%m-%d') > datetime.now() - relativedelta(years=13):
                errors.append("You must be at least 13 y/o.")
        except ValueError: 
            errors.append("Please enter a valid date")

        if len(errors) > 0:
            return (False, errors)
        else:
            u = User.objects.create(name=postData['name'], username=postData['user_name'], email=postData['email'], password=postData['password'], birthday=postData['birthday'])
            return (True, u)

    def login_validation(self, postData):

        errors = []
        if len(postData['user_name']) < 2:
            errors.append("Your username is too short")
        if len(postData['password']) < 2:
            errors.append("Your password is too short")

        if len(errors) > 0:
            return (False, errors)
        else:
            u = User.objects.filter(username=postData['user_name'])
            # QuerySet[<User Obj>]
            if u: # check to see if i got a user based on username
                print "found a user", 0
                if u[0].password == postData['password']: 
                    # if true, username and password matches what is in DB
                    return (True, u[0]) # <User Obj>
                    
                else:
                    errors.append("Password is incorrect") 
                    return(False, errors)
            else:
                print "did not find user"
                errors.append("No user exists with this username.") 
                return(False, errors)  
        
    
        
class User(models.Model):
    name = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    birthday = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
	    return 'name: {}, username: {}, email: {}'.format(self.name, self.username, self.email)


class Friend(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user")
    to_user = models.ForeignKey(User, related_name="to_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)