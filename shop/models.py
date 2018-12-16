from django.db import models
from django.urls import reverse


#Variables

TAMANIOS = (('variante_50', '50 mm x 50 mm',), ('variante_75', '75 mm x 75 mm',),
            ('variante_100', '100 mm x 100 mm',), ('variante_125', '125 mm x 125 mm',))

CANTIDADES = (('cantidad_50', '50',), ('cantidad_100', '100',),
              ('cantidad_200', '200',), ('cantidad_300', '300',),
              ('cantidad_500', '500',), ('cantidad_1000', '1000',),
              ('cantidad_2000', '2000',), ('cantidad_3000', '3000',),
              ('cantidad_4000', '4000',), ('cantidad_5000', '5000',),
              ('cantidad_1000', '1000',))


# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('shop:products_by_category', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_url(self):
        return reverse('shop:ProdCatDetail', args=[self.category.slug, self.slug])

    def __str__(self):
        return '{}'.format(self.name)


# class SizeQuantity(models.Model):
#
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     size = models.CharField(max_length=10, choices=TAMANIOS)
#     quantity = models.CharField(max_length=10, choices=CANTIDADES)
#     image = models.ImageField(upload_to='images', blank=True, null=True)
#     # imagenes = models.ImageField(upload_to='category', blank=True)
#     # comment = models.CharField(max_length=200, blank=True, null=True, default='')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.size