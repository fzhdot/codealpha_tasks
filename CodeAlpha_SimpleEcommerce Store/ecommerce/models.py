from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('bagues', 'Bagues'),
        ('colliers', 'Colliers'),
        ('bracelets', 'Bracelets'),
        ('boucles', 'Boucles d\'oreilles'),
        ('sacs', 'Sacs'),
        ('autres', 'Autres accessoires'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='autres',
        verbose_name="Catégorie"
    )
    is_new = models.BooleanField(default=False, verbose_name="Nouveau produit")
    discount = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Remise en pourcentage"
    )

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount / 100)
        return self.price
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
