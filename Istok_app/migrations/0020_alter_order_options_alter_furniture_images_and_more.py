# Generated by Django 4.2 on 2024-08-19 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Istok_app', '0019_order_delete_application_remove_parts_order_number_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='furniture',
            name='images',
            field=models.ManyToManyField(related_name='furniture_images', through='Istok_app.FurnitureImage', to='Istok_app.projectimage', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='order',
            name='create_date',
            field=models.DateField(null=True, verbose_name='Дата заказа'),
        ),
        migrations.CreateModel(
            name='OrderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Istok_app.order')),
                ('order_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Istok_app.projectimage')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='images',
            field=models.ManyToManyField(related_name='order_images', through='Istok_app.OrderImage', to='Istok_app.projectimage', verbose_name='Изображение заказа'),
        ),
    ]
