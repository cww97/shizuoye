# -*-coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import BaseValidator
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^[a-zA-Z\_]+[\w]+$'
    message = _(
        '用户名可以包含字母、数字和下划线，且必须字母或者下划线开头'
    )


username_min_len = 5
class UsernameLengthValidator(BaseValidator):
    message = _("Username should contain at least %d characters." % username_min_len)
    code = 'min_length'

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        try:
            return len(x.encode("GBK"))
        except UnicodeEncodeError:
            return len(x)


class User(AbstractUser):
    username_validators = [UsernameValidator(), UsernameLengthValidator(username_min_len)]

    username = models.CharField("用户名", max_length=30, unique=True,
                              validators=username_validators,
                              error_messages={
                                'unique': _("A user with that username already exists.")}
                              )
    phone = PhoneNumberField("手机号码", region='CN', blank=True, unique=True)
    email = models.EmailField("邮箱", max_length=192, blank=True, error_messages={
        'unique': _("This email has already been used.")
    })
    school = models.CharField("学校", max_length=64, blank=True)
    name = models.CharField("真实姓名", max_length=30, blank=True)
    student_id = models.CharField("学号", max_length=30, blank=True)
    motto = models.CharField("警句", max_length=192, blank=True)
    
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    polygon_enabled = models.BooleanField(default=False)

    avatar = models.ImageField("头像", upload_to='avatar', default='avatar/default.jpg')
    avatar_small = ImageSpecField(source='avatar', processors=[ResizeToFill(50, 50)],
                                format='JPEG',  options={'quality': 60})
    avatar_large = ImageSpecField(source='avatar',processors=[ResizeToFill(500, 500)],
                                format='JPEG', options={'quality': 60})

    def __str__(self):
        return self.username

    def has_coach_access(self):
        return self.polygon_enabled