from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='название категории')
    description = models.TextField(blank=True, verbose_name='описание категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=128, verbose_name='название товара')
    image = models.ImageField(upload_to='products_images', blank=True, verbose_name='изображение')
    short_desc = models.CharField(max_length=128, blank=True, verbose_name='краткое описание')
    description = models.TextField(blank=True, verbose_name='описание товара')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.name} ({self.category.name})'
