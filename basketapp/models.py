from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product

# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super(BasketQuerySet, self).delete(*args, **kwargs)

class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    add_date_time = models.DateTimeField(auto_now_add=True, verbose_name='время добавления')

    class Meta:
        verbose_name = 'корзинка'
        verbose_name_plural = 'корзинки'

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @property
    def total_quantity(self):
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()

    # def save(self):
    #     if self.pk:
    #         self.product.quantity = self.quantity - self.__class__.gi