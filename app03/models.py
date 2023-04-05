from django.db import models


class Admin(models.Model):
    username = models.CharField(verbose_name="username", max_length=32)
    password = models.CharField(verbose_name="password", max_length=32)

    def __str__(self):
        return self.username
