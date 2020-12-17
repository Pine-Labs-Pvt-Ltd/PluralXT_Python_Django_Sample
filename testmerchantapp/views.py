from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import MerchantTestPageForm
import hmac
import hashlib 
import binascii
import requests
import json
import base64

# Create your views here.

@csrf_exempt
def merchant_test_page(request):
	if request.method == "POST":
		form = MerchantTestPageForm(request.POST)
		if form.is_valid():
			data = request.POST

			#setting session variable to be used in another view
			request.session['merchant_secret_key'] = data['merchant_secret_key']

			tempObj = {
			  "merchant_data": {
			    "merchant_return_url": data['merchant_return_url'],
			    "merchant_access_code": data['merchant_access_code'],
			    "order_id": data['order_id'],
			    "merchant_id": data['merchant_id']
			  },
			  "payment_info_data": {
			    "amount": data['amount_in_paisa'],
			    "currency_code": "INR",
			    "preferred_gateway": data['preferred_payment_gateway'],
			    "order_desc": data['order_description']
			  },
			  "customer_data": {
			    "customer_ref_no": data['customer_ref_no'],
			    "mobile_number": data['customer_mobile_number'],
			    "email_id": data['customer_email_id'],
			    "first_name": data['customer_first_name'],
			    "last_name": data['customer_last_name'],
			    "country_code": "91",
			  },
			  "billing_address_data": {
			    "first_name": data['billing_first_name'],
			    "last_name": data['billing_last_name'],
			    "address1": data['billing_address1'],
			    "address2": data['billing_address2'],
			    "address3": data['billing_address3'],
			    "pincode": data['billing_pincode'],
			    "city": data['billing_city'],
			    "state": data['billing_state'],
			    "country": data['billing_country']
			  },
			  "shipping_address_data": {
			    "first_name": data['shipping_first_name'],
			    "last_name": data['shipping_last_name'],
			    "address1": data['shipping_address1'],
			    "address2": data['shipping_address2'],
			    "address3": data['shipping_address3'],
			    "pincode": data['shipping_pincode'],
			    "city": data['shipping_city'],
			    "state": data['shipping_state'],
			    "country": data['shipping_country']
			  },
			  "product_info_data": {
			    "product_details": [
			      {
			        "product_code": data['product_code'],
			        "product_amount": data['product_amount_in_paisa']
			      }
			    ]
			  },
			  "additional_info_data": {
			    "rfu1": ''
			  }
			}

			order_request = json.dumps(tempObj)

			#base64 encoding
			order_request = order_request.encode()
			order_request = base64.encodestring(order_request)
			order_request = order_request.decode()
			
			#x-verify header
			x_verify = generate_hash(data['merchant_secret_key'], order_request)

			rapidpay_host_url = 'https://paymentoptimizer.pinepg.in'

			if data['is_production'] == 0:
				rapidpay_host_url = 'https://paymentoptimizertest.pinepg.in'

			order_creation_api = rapidpay_host_url + '/api/v2/order/create'

			body =	{
						"request": order_request 
					}
			headers = {'content-type': 'application/json', 'X-VERIFY': x_verify}

			#create order
			response = requests.post(order_creation_api, data = json.dumps(body), headers = headers)
			
			order_creation_response = response.json()

			if 'token' in order_creation_response:
				token = order_creation_response['token']
				rapidpay_redirect_url = rapidpay_host_url + '/pinepg/v2/process/payment/redirect?orderToken=' + token + '&paymentmodecsv=' + data['payment_modes_csv']

				#redirect to payment page
				return redirect(rapidpay_redirect_url)
			else:
				strMsgResponse = '<h1> RESPONSE PARAMETERS </h1>'

				for key in order_creation_response:
					strMsgResponse += "<strong>" + str(key) + "</strong>" + " = " + str(order_creation_response[key]) +"<BR />"
				
				strMsgResponse += "<BR />" + "<h4>" + "Order Creation Failed" + "</h4>" + "<BR />"

				return render(request, 'testmerchantapp/MerchantResponsePage.html', {'responseHTML': strMsgResponse, 'title': 'Merchant Response Page'})

	else:
		form = MerchantTestPageForm()

	return render(request, 'testmerchantapp/MerchantTestPage.html', {'form': form, 'title': 'Merchant Test Page'})

@csrf_exempt
def merchant_response_page(request):
	strMsgResponse = "<h1> RESPONSE PARAMETERS </h1>"

	request.POST = request.POST.copy()
	data = request.POST
	
	for key in sorted(data):
		strMsgResponse += "<strong>" + key + "</strong>" + " = " + data[key] +"<BR />"
	
	strSecretKey = request.session.get('merchant_secret_key', -1)
	# strHashType = "SHA256"

	if strSecretKey != -1:
		msgString = ""
		
		for key in sorted(data):
			if data[key] != None and key != 'dia_secret' and key != 'dia_secret_type':
				msgString += str(key) + "=" + str(data[key]) + "&"

		msgString = msgString[:-1]

		strDIA_SECRET = generate_hash(strSecretKey, msgString)

		strMsgResponse += "<strong>" + "Hash Generated on Response Page" + "</strong>" + " = " + strDIA_SECRET +"<BR />"
		strMsgResponse += "<strong>" + "Do Hashes match?: " + "</strong>"

		comment = ""

		if (strDIA_SECRET == data['dia_secret']):
			#Transaction is successful if payment_status = "CAPTURED" and payment_response_code = 1
			if (data['payment_status'] == "CAPTURED" and data['payment_response_code'] == "1"):
				comment = "Transaction SUCCESSFUL"
				strMsgResponse += "YES" + "<BR />"
			else:
				comment = "Transaction UNSUCCESSFUL"
				strMsgResponse += "YES" + "<BR />"
		else:
			comment = "Transaction UNSUCCESSFUL"	#because hashes do not match
			strMsgResponse += "NO" + "<BR />"

		strMsgResponse += "<BR />" + "<h4>" + comment + "</h4>" + "<BR />"

	return render(request, 'testmerchantapp/MerchantResponsePage.html', {'responseHTML': strMsgResponse, 'title': 'Merchant Response Page'})

def generate_hash(key, message):
	byte_key = binascii.unhexlify(key)
	message = message.encode()

	return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()