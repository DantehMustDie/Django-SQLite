# Generated by Django 4.1.4 on 2023-01-10 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0003_alter_deliverys_courier_alter_deliverys_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='apartment',
            field=models.IntegerField(verbose_name='Квартира'),
        ),
        migrations.AlterField(
            model_name='users',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom.citys', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='users',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom.countrys', verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='users',
            name='house',
            field=models.IntegerField(verbose_name='Дом'),
        ),
        migrations.AlterField(
            model_name='users',
            name='index',
            field=models.IntegerField(verbose_name='Индекс'),
        ),
        migrations.AlterField(
            model_name='users',
            name='liter',
            field=models.CharField(max_length=10, verbose_name='Литер'),
        ),
        migrations.AlterField(
            model_name='users',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=20, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.IntegerField(verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='users',
            name='street',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom.streets', verbose_name='Улица'),
        ),
        migrations.AlterField(
            model_name='users',
            name='surname',
            field=models.CharField(max_length=40, verbose_name='Фамилия'),
        ),
    ]