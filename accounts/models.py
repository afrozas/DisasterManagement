from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_num, password, **extra_fields):
        if not phone_num:
            raise ValueError('Phone Number must be specified.')
        user = self.model(phone_num=phone_num, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, phone_num, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_num, password, **extra_fields)

    def create_superuser(self, phone_num, password, **extra_fields):
        print(extra_fields)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(phone_num, password, **extra_fields)


class User(AbstractBaseUser):
    """Profile of a user in the site."""
    phone_num = models.CharField(unique=True, max_length=15)
    address = models.TextField(max_length=500, blank=True)
    last_known_latitude = models.DecimalField(max_digits=9,
                                              decimal_places=6,
                                              verbose_name='latitude',
                                              null=True)
    last_known_longitude = models.DecimalField(max_digits=9,
                                               decimal_places=6,
                                               verbose_name='longitude',
                                               null=True)
    is_safe = models.NullBooleanField(blank=True)
    watching = models.ManyToManyField('self',
                                      related_name='watchers',
                                      blank=True)

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_num'
    EMAIL_FIELD = 'phone_num'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_is_safe = False

    def save(self, *args, **kwargs):
        if not self.prev_is_safe and self.is_safe:
            self.notify_watchers()
            self.prev_is_safe = True
        super().save(*args, **kwargs)

    def notify_watchers():
        pass
