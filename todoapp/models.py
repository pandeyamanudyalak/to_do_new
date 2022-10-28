from email.policy import default
from random import choices
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.



class UserManager(BaseUserManager):
  def create_user(self, email, password=None):
     
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          password=password,
          
         
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, password=None):
     
      user = self.create_user(
          email,
          password=password,
        
          
          
      )
      user.is_active = True
      user.is_admin = True
      #user.is_staff = True
      user.save(using=self._db)
      return user







class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
 
  password = models.CharField(max_length=200)
  is_email_verified = models.BooleanField(default=False)
  otp = models.IntegerField(null=True,blank=True)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  

 

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['password']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin


class Tasks(models.Model):
    
    task_user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    #due_date = models.DateField()
    description = models.CharField(max_length=500)
    is_completd = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

   

class SharedTasks(models.Model):
    to_user = models.ForeignKey(User,on_delete=models.CASCADE)
    tasks = models.ForeignKey(Tasks,on_delete=models.CASCADE)
    assigned_by = models.CharField(max_length=100)
    read_only = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    notify = models.BooleanField(default=False)
    title = models.CharField(max_length=100,default='new')
    description = models.CharField(max_length=500,default="new_task")


    def __str__(self):
        return str(self.to_user)


