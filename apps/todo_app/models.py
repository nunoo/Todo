from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#-------------------------------------------------------------------------------
#User
#-------------------------------------------------------------------------------

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Invalid First Name! - Must be 2 characters long"
        if not (postData['first_name'].isalpha()) == True:
            errors['first_name'] = "Invalid First Name! - Can only contain alphabetic characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Invalid Last Name! - Must be 2 characters long"
        if not (postData['last_name'].isalpha()) == True:
            errors['last_name'] = "Invalid Last Name! - Can only contain alphabetic characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        emailAlreadyExists = User.objects.filter(email = postData['email']).exists()
        if (emailAlreadyExists):
            errors['email'] = "Email already in system"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['pwconfirm']:
            errors['confirmpw'] = "Password and Confirm Password must match"
        return errors

    def login_validator(self, postData):
        errors = {}
        loginemailAlreadyExists = User.objects.filter(email = postData['emailLogin']).exists()
        if len(postData['emailLogin']) < 1:
            errors['loginemail_void'] = "Failure to login"
        elif len(postData['emailLogin']) > 1 and not (loginemailAlreadyExists):
            errors['loginemail'] = "Failure to login"
        else:
            user = User.objects.get(email=postData["emailLogin"])
            pw_to_hash = postData["passwordLogin"]
            if not bcrypt.checkpw(pw_to_hash.encode(), user.password.encode()):
                errors['loginemail'] = "Failure to login"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    # member_of
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return f"<User object: FN: {self.first_name} LN: {self.last_name} EM: {self.email} PW: {self.password} ID: ({self.id})>"


class GroupManager(models.Manager):
    def group_validator(self, postData):
        errors = {}
        if len(postData['group_name']) < 2:
            errors['group_name'] = "Invalid Group Name! - Must be 2 characters long"
        groupAlreadyExists = Group.objects.filter(group_name = postData['group_name']).exists()
        if (groupAlreadyExists):
            errors['group_name'] = "Group already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['pwconfirm']:
            errors['confirmpw'] = "Password and Confirm Password must match"
        return errors

    def group_login_validator(self, postData):
        errors = {}
        logingroupAlreadyExists = Group.objects.filter(group_name = postData['groupLogin']).exists()
        if not (logingroupAlreadyExists):
            errors['logingroup'] = "Failure to login"
        else:    
            group = Group.objects.get(group_name=postData['groupLogin'])
            pw_to_hash = postData["passwordLogin"]
            if not bcrypt.checkpw(pw_to_hash.encode(), group.password.encode()):
                errors['logingroup'] = "Failure to login"
        return errors


class Group(models.Model):
    group_name = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    members = models.ManyToManyField(User, related_name='member_of')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GroupManager()
    def __repr__(self):
        return f'<User object: GN: {self.group_name} Members: {self.members} >'


    