import uuid
import json
from django.db import models
from django.db.models.base import Model
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import serializers, status, generics, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from user_app.models import UserProfile
from wallet_app.models import Wallet, WalletTransaction
from .serializers import UserProfileSerializers, WalletSerializers, WalletTransactionSerializers

# Create your views here.
class CreateUser(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializers(data=request.data)
        if serializer.is_valid():
            try:
                user = UserProfile.objects.get(customer_xid=serializer.data['customer_xid'])
                token = Token.objects.get(user=user.user)
                response = {
                    "data": {
                        "token": token.key
                    }, 
                    "status": "success"
                }
                return Response(response, status=status.HTTP_302_FOUND)
            except UserProfile.DoesNotExist as e:
                user = User.objects.create_user(f"{uuid.uuid4()}")
                user.save()
                user_profile = UserProfile.objects.create(user=user, customer_xid=serializer.data['customer_xid'])
                user_profile.save()
                token = Token.objects.create(user=user)
                token.save()
                response = {
                    "data": {
                        "token": token.key
                    }, 
                    "status": "success"
                }
                return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "data" : {
                "error" : serializer.errors
            },
            "status" : "fail"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# TODO
class EnableWallet(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        user = Token.objects.get(key=token).user
        wallet = Wallet.objects.get(owned_by=user)
        response = {
            "status": "success",
            "data": {
                "wallet": {
                "id": str(wallet.id),
                "owned_by": str(wallet.owned_by),
                "status": "enabled" if wallet.status == True else "disabled",
                "enabled_at": wallet.enable_at,
                "balance": wallet.balance
                }
            }
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        user = Token.objects.get(key=token).user

        try:
            wallet = Wallet.objects.get(owned_by=user)
            wallet.status = True
            wallet.save()
            response = {
                "status": "success",
                "data": {
                    "wallet": {
                    "id": str(wallet.id),
                    "owned_by": str(wallet.owned_by),
                    "status": "enabled" if wallet.status == True else "disabled",
                    "enabled_at": wallet.enable_at,
                    "balance": wallet.balance
                    }
                }
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Wallet.DoesNotExist as e:
            wallet = Wallet.objects.create(owned_by=user, status=True, balance=0)
            wallet.save()
            response = {
                "status": "success",
                "data": {
                    "wallet": {
                    "id": str(wallet.id),
                    "owned_by": str(wallet.owned_by),
                    "status": "enabled" if wallet.status == True else "disabled",
                    "enabled_at": wallet.enable_at,
                    "balance": wallet.balance
                    }
                }
            }
            return Response(response, status=status.HTTP_201_CREATED)


class DepositMoney(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        user = Token.objects.get(key=token).user
        wallet = Wallet.objects.get(owned_by=user)
        serializer = WalletTransactionSerializers(data=request.data)
        if serializer.is_valid() and wallet.status == True:
            wallet.balance += serializer.data['ammount']
            wallet.save()
            wallet_transaction = WalletTransaction.objects.create(user=user, 
                                                                  wallet=wallet, 
                                                                  transaction_type="+", 
                                                                  ammount=serializer.data['ammount'], 
                                                                  reference_id=serializer.data['reference_id'])
            wallet_transaction.save()
            response = {
                "status": "success",
                "data": {
                    "deposit": {
                    "id": str(wallet.id),
                    "deposited_by": str(wallet_transaction.user),
                    "status": "success",
                    "deposited_at": wallet_transaction.timestamp,
                    "amount": serializer.data['ammount'],
                    "reference_id": str(wallet_transaction.reference_id)
                    }
                }
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawMoney(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        user = Token.objects.get(key=token).user
        wallet = Wallet.objects.get(owned_by=user)
        serializer = WalletTransactionSerializers(data=request.data)
        if wallet.status == True and serializer.is_valid():
            wallet.balance -= serializer.data['ammount']
            wallet.save()
            wallet_transaction = WalletTransaction.objects.create(user=user, 
                                                                wallet=wallet, 
                                                                transaction_type="-", 
                                                                ammount=serializer.data['ammount'], 
                                                                reference_id=serializer.data['reference_id'])
            wallet_transaction.save()
            response = {
                "status": "success",
                "data": {
                    "deposit": {
                    "id": str(wallet.id),
                    "deposited_by": str(wallet_transaction.user),
                    "status": "success",
                    "deposited_at": wallet_transaction.timestamp,
                    "amount": serializer.data['ammount'],
                    "reference_id": str(wallet_transaction.reference_id)
                    }
                }
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)