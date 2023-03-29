from django.db import models
from django.utils import timezone


# Create your models here.
class Department(models.Model):
    department = models.CharField(verbose_name="部门", max_length=32, unique=True)

    def __str__(self):  # 修改print出来的值
        return self.department


class Employee(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=16)
    pwd = models.CharField(verbose_name="密码", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    balance = models.DecimalField(verbose_name="工资余额", max_digits=10, decimal_places=2, default=0)
    department = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", blank=True, null=True,
                                   on_delete=models.SET_NULL)
    gender_choices = ((1, "male"), (2, "female"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    register_time = models.DateTimeField(verbose_name="入职时间", default=timezone.now)


class Task(models.Model):
    title = models.CharField(verbose_name="标题", max_length=16)
    level_choice = ((1, "紧急"), (2, "普通"), (3, "临时"))
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice)
    detail = models.TextField(verbose_name="详细信息", max_length=200)
    user = models.ForeignKey(verbose_name="负责人", to="app03.Admin", on_delete=models.CASCADE)


class Order(models.Model):
    order_number = models.CharField(verbose_name="订单号", max_length=64)
    name = models.CharField(verbose_name="商品名称", max_length=12)
    price = models.IntegerField(verbose_name="价格")
    status_choice = ((1, "已支付"), (2, "待支付"))
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice)
    customer_id = models.ForeignKey(to="app03.Admin", verbose_name="用户ID", on_delete=models.CASCADE)
