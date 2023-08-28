from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,name, password=None, is_staff=False):

        if not email:
            raise ValueError('Users must have an email address!')

        user  = self.model(email= self.normalize_email(email), name= name,)

        user.set_password(password)
        user.is_staff = is_staff
        user.save(using= self.db)
        return user

    def create_superuser(self,email, name, password=True, is_staff=True, *args, **kwargs):
        user = self.create_user(
            email,
            password= password,
            name= name,
        )

        # user.is_admin = True
        user.is_superuser = True
        user.is_staff = is_staff
        user.save(using= self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Email', 
        max_length=255,
        unique=True
    )
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField()

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'is_staff', 'email',]
