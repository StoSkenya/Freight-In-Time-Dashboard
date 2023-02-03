# manager for our custom user
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _



# manager class
class CustomUserManager(BaseUserManager):
    """
        we will set the email as the unique identifier
    """
    def create_user(self,email,password,**kwargs):
        """
            create and save user with email and pswrd
        """
        if not email:
            raise ValueError(_('You must set your mail '))
        
        email = self.normalize_email(email)
        user = self.model(email=email,**kwargs)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self,email,password,**kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        kwargs.setdefault('is_active',True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **kwargs)