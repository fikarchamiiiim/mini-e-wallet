from django.db.models import fields
from rest_framework import serializers
from user_app.models import UserProfile
from wallet_app.models import Wallet, WalletTransaction

class UserProfileSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ['customer_xid']

class WalletSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Wallet
        fields = ['id', 'owned_by', 'status', 'enable_at', 'balance']

class WalletTransactionSerializers(serializers.ModelSerializer):

    class Meta:
        model = WalletTransaction
        fields = ["ammount", "reference_id"]