from django.db import models


# Create your models here.
# class Account(models.Model):
#     mobile = models.CharField(verbose_name="账号", max_length=11)
#     price = models.IntegerField(verbose_name="价格")
#     level_choices = ((1, "至尊"), (2, "高级"), (3, "普通"), (4, "垃圾"))
#     level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=4)
#     status_choices = ((1, "占用"), (2, "未占用"))
#     status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)
#

class Admin(models.Model):
    username = models.CharField(verbose_name="username", max_length=32)
    password = models.CharField(verbose_name="password", max_length=32)

    def __str__(self):
        return self.username
