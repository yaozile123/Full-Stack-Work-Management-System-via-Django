from django.db import models
from django.utils import timezone


# Create your models here.
class Department(models.Model):
    department = models.CharField(verbose_name="Department", max_length=32, unique=True)

    def __str__(self):  # 修改print出来的值
        return self.department


class Employee(models.Model):
    name = models.CharField(verbose_name="Name", max_length=16)
    pwd = models.CharField(verbose_name="Password", max_length=32)
    age = models.IntegerField(verbose_name="Age")
    balance = models.DecimalField(verbose_name="Balance", max_digits=10, decimal_places=2, default=0)
    department = models.ForeignKey(verbose_name="Department", to="Department", to_field="id", blank=True, null=True,
                                   on_delete=models.SET_NULL)
    gender_choices = ((1, "male"), (2, "female"))
    gender = models.SmallIntegerField(verbose_name="Gender", choices=gender_choices)
    register_time = models.DateTimeField(verbose_name="Joining Date", default=timezone.now)


class Task(models.Model):
    title = models.CharField(verbose_name="Title", max_length=16)
    level_choice = ((1, "紧急"), (2, "普通"), (3, "临时"))
    level = models.SmallIntegerField(verbose_name="Level", choices=level_choice)
    detail = models.TextField(verbose_name="Details", max_length=200)
    user = models.ForeignKey(verbose_name="负责人", to="app03.Admin", on_delete=models.CASCADE)


class Order(models.Model):
    order_number = models.CharField(verbose_name="Order No.", max_length=64)
    name = models.CharField(verbose_name="Product Name", max_length=12)
    price = models.IntegerField(verbose_name="Price")
    status_choice = ((1, "Paid"), (2, "Unpaid"))
    status = models.SmallIntegerField(verbose_name="Status", choices=status_choice)
    customer_id = models.ForeignKey(to="Customer", verbose_name="Customer ID", on_delete=models.CASCADE)


class Customer(models.Model):
    username = models.CharField(verbose_name="Username", max_length=64)
    birthdate = models.DateField(verbose_name="Birthdate", default=timezone.now)
    age = models.IntegerField(verbose_name="Age")
    level_choice = ((1, "Platinum"), (2, "Gold"), (3, "Silver"), (4, "Bronze"))
    level = models.SmallIntegerField(verbose_name="Level", choices=level_choice)

    def __str__(self):  # 修改print出来的值
        return self.username

