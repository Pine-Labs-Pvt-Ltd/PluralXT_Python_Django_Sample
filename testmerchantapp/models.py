from django.db import models
from django.db.models import CharField


class MerchantTestPage(models.Model):
    merchant_id = CharField(max_length=200)
    merchant_access_code = CharField(max_length=200)
    merchant_secret_key = CharField(max_length=200)
    merchant_return_url = CharField(max_length=200)
    payment_modes_csv = CharField(max_length=200)
    is_production = CharField(max_length=200)
    preferred_payment_gateway = CharField(max_length=200)
    order_id = CharField(max_length=200)
    amount_in_paisa = CharField(max_length=200)
    order_description = CharField(max_length=200)
    customer_ref_no = CharField(max_length=200)
    customer_first_name = CharField(max_length=200)
    customer_last_name = CharField(max_length=200)
    customer_mobile_number = CharField(max_length=200)
    customer_email_id = CharField(max_length=200)
    billing_first_name = CharField(max_length=200)
    billing_last_name = CharField(max_length=200)
    billing_address1 = CharField(max_length=200)
    billing_address2 = CharField(max_length=200)
    billing_address3 = CharField(max_length=200)
    billing_pincode = CharField(max_length=200)
    billing_city = CharField(max_length=200)
    billing_state = CharField(max_length=200)
    billing_country = CharField(max_length=200)
    shipping_first_name = CharField(max_length=200)
    shipping_last_name = CharField(max_length=200)
    shipping_address1 = CharField(max_length=200)
    shipping_address2 = CharField(max_length=200)
    shipping_address3 = CharField(max_length=200)
    shipping_pincode = CharField(max_length=200)
    shipping_city = CharField(max_length=200)
    shipping_state = CharField(max_length=200)
    shipping_country = CharField(max_length=200)
    product_code = CharField(max_length=200)
    product_amount_in_paisa = CharField(max_length=200)
    # rfu1 = CharField(max_length=200) 

    def __str__(self):
       return self.title
