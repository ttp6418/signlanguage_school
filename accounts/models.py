from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

# Create your models here.

class language(models.Model):
    language_name = models.CharField(max_length=20, primary_key=True, default="한국어")
    language_function = models.CharField(max_length=10)

from django.contrib.auth.models import AbstractUser

class user(AbstractUser):
    # 상속받은 테이블
    # 기본적으로 제공하는 필드 외에 필드 추가함.
    # user_name = models.CharField(max_length=40)
    user_nickname = models.CharField(max_length=10)
    user_phoneNumber = models.CharField(validators = [RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')], max_length = 16, null=True, default="00000000000", unique=False)   # dummy, 나중에 사용시 unique=True
    user_birthDate = models.DateField(null=True)                                                                                                                # dummy
    user_nationality = models.CharField(max_length=10, default='N/A')
    user_sex = models.CharField(max_length=1, default='s')
    user_language = models.ForeignKey(language, related_name="language", on_delete=models.DO_NOTHING, default='')