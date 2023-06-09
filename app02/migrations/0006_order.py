# Generated by Django 4.1.7 on 2023-03-23 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app03', '0004_admin_alter_account_level_alter_account_mobile_and_more'),
        ('app02', '0005_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=64, verbose_name='订单号')),
                ('name', models.CharField(max_length=12, verbose_name='商品名称')),
                ('price', models.IntegerField(verbose_name='价格')),
                ('status', models.SmallIntegerField(choices=[(1, '已支付'), (2, '待支付')], verbose_name='状态')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app03.admin', verbose_name='用户ID')),
            ],
        ),
    ]
