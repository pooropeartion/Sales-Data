from django.db import models

# Create your models here.



from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    promotion_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    net_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    region = models.CharField(max_length=1, choices=[('A', 'Region A'), ('B', 'Region B')])

    def __str__(self):
        return f"Order {self.order_id} - Region {self.region}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem {self.id} - Order {self.order.order_id}"



class Joke(models.Model):
    setup = models.CharField(max_length=255, blank=True, null=True)
    punchline = models.CharField(max_length=255, blank=True, null=True)
    joke_text = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    nsfw = models.BooleanField(default=False)
    political = models.BooleanField(default=False)
    sexist = models.BooleanField(default=False)
    safe = models.BooleanField(default=False)
    lang = models.CharField(max_length=10)

    def __str__(self):
        return self.joke_text if self.joke_text else f"{self.setup} - {self.punchline}"