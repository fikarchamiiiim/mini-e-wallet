from django.urls import path
from api_app.views import CreateUser, EnableWallet, DepositMoney, WithdrawMoney

urlpatterns = [
    path('v1/init/', CreateUser.as_view(), name="create_user"),
    path('v1/wallet/', EnableWallet.as_view(), name="enable_wallet"),
    path('v1/wallet/deposits/', DepositMoney.as_view(), name="deposit_money"),
    path('v1/wallet/withdraws/', WithdrawMoney.as_view(), name="withdraw_money"),
]
