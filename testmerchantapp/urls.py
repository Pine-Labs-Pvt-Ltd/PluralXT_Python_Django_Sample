from django.urls import path
from . import views

urlpatterns = [
	path('MerchantTestPage/', views.merchant_test_page, name = 'merchant_test_page'),
	path('MerchantResponsePage/', views.merchant_response_page, name = 'merchant_response_page'),
]
