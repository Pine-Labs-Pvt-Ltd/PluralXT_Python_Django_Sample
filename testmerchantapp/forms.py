from django import forms
from .models import MerchantTestPage

class MerchantTestPageForm(forms.ModelForm):
	class Meta:
		model = MerchantTestPage
		fields = (
					'merchant_id',
					'merchant_access_code',
					'merchant_secret_key',
					'merchant_return_url',
					'payment_modes_csv',
					'is_production',
					'preferred_payment_gateway',
					'order_id',
					'amount_in_paisa',
					'order_description',
					'customer_ref_no',
					'customer_first_name',
					'customer_last_name',
					'customer_mobile_number',
					'customer_email_id',
					'billing_first_name',
					'billing_last_name',
					'billing_address1',
					'billing_address2',
					'billing_address3',
					'billing_pincode',
					'billing_city',
					'billing_state',
					'billing_country',
					'shipping_first_name',
					'shipping_last_name',
					'shipping_address1',
					'shipping_address2',
					'shipping_address3',
					'shipping_pincode',
					'shipping_city',
					'shipping_state',
					'shipping_country',
					'product_code',
					'product_amount_in_paisa'
					# 'rfu1'
				)