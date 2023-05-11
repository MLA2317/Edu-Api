from django.db import models
# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import post_save, pre_save

Profile = settings.AUTH_USER_MODEL


def image_path(instance, filename):
    return f"account/{instance.id}/{filename}"

class AccountManager(BaseUserManager): # manager - bu user model un yordamchi class, user model create qilish un qonun qoidalarini toplami
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError('User should have a email')

        user = self.model(email=email, **extra_fields) # user yasavolamiz
        user.set_password(password)
        user.save(using=self._db) # db - bu settingdagi defoult database dan foydalansin
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if password is None:
            raise TypeError("Password should not be None")

        user = self.create_user(
            email=email,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active =True
        user.role = 2
        user.save(using=self._db)
        return user


# 2 usul ozimiz user yaratamiz
class Account(AbstractBaseUser, PermissionsMixin):
    ROLE = (
        (0, 'Teacher'),
        (1, 'Student'),
        (2, 'Staff'),
    )
    email = models.EmailField(max_length=50, unique=True, verbose_name='Email', db_index=True) # unique - bu har bitta emailda boshqa user qayta osha emaildan foydalanomidi
    first_name = models.CharField(max_length=50 , verbose_name='first_name', null=True)
    last_name = models.CharField(max_length=50 , verbose_name='last_name', null=True)
    image = models.ImageField(upload_to=image_path)  # username/filename.png
    bio = models.TextField()
    role = models.IntegerField(choices=ROLE, default=0)
    is_superuser = models.BooleanField(default=False, verbose_name='Super user')
    is_staff = models.BooleanField(default=False, verbose_name='Staff user')
    is_active = models.BooleanField(default=False, verbose_name='Active user')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date Modified')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')

    objects = AccountManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name } {self.last_name}"
        return f"{self.email}"

    def image_tag(self):
        if self.image:
            return mark_safe(f"<a href='{self.image.url}'><img src='{self.image.url}' style='height:43px;'/></a>")
        else:
            return 'Image not found'


    @property
    def image_url(self):
        if self.image:
            if settings.DEBUG:
                return f"{settings.LOCALE_BASE_URL}{self.image.url}"
            return f"{settings.PROD_BASE_URL}{self.image.url}"
        return None

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh), # bu - access token ni yangilab beradi
            'access': str(refresh.access_token) # bu - saytga kirish un ruhsat
        }
        return data


def account_post_save(instance, sender, *args, **kwargs):
    if instance.role == 2:
        instance.is_staff = True
    else:
        instance.is_staff = False
    return instance


pre_save.connect(account_post_save, sender=Account)

# 1 usul, Tayor ktubxonadan Yozilgan
#
# class Profile(models.Model):
#     ROLE = (
#         (0, 'Teacher'),
#         (1, 'Student'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=image_path)  # username/filename.png
#     bio = models.TextField()
#     role = models.IntegerField(choices=ROLE, default=1)
#
#     def __str__(self):
#         return self.user.username
#
#     def image_tag(self):
#         if self.image:
#             return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" style="height:43px;"/></a>')
#         else:
#             return 'Image not found'
#
#
# def user_post_save(instance, sender, created, *args, **kwargs):
#     if created:
#         Profile.objects.create(user_id=instance.id)
#
#
# post_save.connect(user_post_save, sender=User)
