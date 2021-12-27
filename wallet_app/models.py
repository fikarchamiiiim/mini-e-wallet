from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Wallet(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    enable_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    balance = models.IntegerField()


    def __str__(self):
        return f"User : {self.owned_by}, wallet : {self.id}"

class WalletTransaction(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=1)
    ammount = models.IntegerField()
    reference_id = models.CharField(max_length=40, default="1")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"{self.user} : {self.transaction_type} {self.ammount}"
