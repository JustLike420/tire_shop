from django.db import models
from django.urls import reverse
from django.conf import settings


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    picture = models.ImageField(
        verbose_name='Изображение',
        upload_to='products',
        default='test.png'
    )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    is_active = models.BooleanField(verbose_name='Статус', default=True)

    def __str__(self):
        return f"Товар: {self.name}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"pk": self.pk})

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={"pk": self.pk})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={"pk": self.pk})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(verbose_name='Статус', default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"1 of {self.product.name}"

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'

    def get_total_item_price(self):
        return self.product.price * self.quantity

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(verbose_name='Статус', default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
