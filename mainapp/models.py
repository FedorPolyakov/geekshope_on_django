from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='название категории')
    description = models.TextField(blank=True, verbose_name='описание категории')
    is_active = models.BooleanField(verbose_name='активна', default=True)

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
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.name} ({self.category.name})

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')

class Locations(models.Model):
    city = models.CharField(max_length=60, verbose_name='город')
    phone = models.CharField(max_length=20, verbose_name='телефон')
    email = models.CharField(max_length=60, verbose_name='эл.почта')
    address = models.CharField(max_length=60, verbose_name='адрес')

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'

    def __str__(self):
        return f'{self.city} - {self.address}'
