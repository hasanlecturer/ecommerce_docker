from django.db import models
from common.helper_timestamp import TimeStampMixin
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()
print(User)


class Cart(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=155, null=True, blank=True)

    class Meta(TimeStampMixin.Meta):
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["-created_at"]

        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=False)
                | models.Q(session_key__isnull=False),
                name="user_or_session_key_required",
            ),
            models.UniqueConstraint(
                fields=["user"],
                name="unique_user_name",
                condition=models.Q(user__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["session_key"],
                name="unique_session_key",
                condition=models.Q(session_key__isnull=False),
            ),
        ]

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}'s Cart"
        return f"Anonymous Cart ({self.session_key})"

    @property
    def is_anonymous(self):
        return self.user is None

    @property
    def has_session_key(self):
        return self.session_key is not None

    @property
    def total_items(self):
        return self.items.aggregate(total=models.Sum("quantity"))["total"] or 0

    @property
    def sub_total(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    @property
    def total(self):
        return self.sub_total

    @property
    def total_discount(self):
        return sum(
            (item.product.price - item.product.discounted_price) * item.quantity
            for item in self.items.all()
            if hasattr(item.product, "discounted_price")
        )

    def assign_to_user(self, user):
        self.user = user
        self.session_key = None
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="cart_items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def item_total(self):
        """Total Price for this Cart Item"""
        return (self.product.discounted_price or self.product.price) * self.quantity
