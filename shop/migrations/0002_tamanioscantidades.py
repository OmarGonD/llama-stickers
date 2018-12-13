# Generated by Django 2.1.3 on 2018-12-11 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TamaniosCantidades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tamanios', models.CharField(choices=[('variante_50', '50 mm x 50 mm'), ('variante_75', '75 mm x 75 mm'), ('variante_100', '100 mm x 100 mm'), ('variante_125', '125 mm x 125 mm')], max_length=10)),
                ('cantidades', models.CharField(choices=[('cantidad_50', '50'), ('cantidad_100', '100'), ('cantidad_200', '200'), ('cantidad_300', '300'), ('cantidad_500', '500'), ('cantidad_1000', '1000'), ('cantidad_2000', '2000'), ('cantidad_3000', '3000'), ('cantidad_4000', '4000'), ('cantidad_5000', '5000'), ('cantidad_1000', '1000')], max_length=10)),
                ('imagenes', models.FileField(blank=True, null=True, upload_to='imagenes/')),
                ('instrucciones', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
            ],
        ),
    ]
