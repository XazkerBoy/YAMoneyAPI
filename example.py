from yamoney import YandexMoney

# Register a new app at https://money.yandex.ru/myservices/new.xml and paste the recieved ID and URL below
ya = YandexMoney("YOUR_CLIENT_ID", redirect_url="URL_SET_IN_REGISTRATION")	# Without token
# If you already recieved the token, you can use the method below
# ya = YandexMoney("YOUR_CLIENT_ID", "YOUR_TOKEN")	# With token
# A confirmation page will be shown where you have to confirm token generation (you will recieve a code on your phone)
# After the confirmation the token will be shown in console - SAVE IT FOR FURTHER USE!!!
# With the token you don't need to specify URL and dont need to confirm new token generation every time
acc_info = ya.getAccInfo()	# Get account info (balance, ID...)
# Each method deliveres response with this structure:
# {'error': 1 (There is an error) / 0 (No errors), 'error_message': '...' (if error occured) / 'data': '...' (returned data if there are no errors)}
if acc_info['error']:
	print('Account data could not be fetched\r\nError: {}'.format(acc_info['error_message']))
	exit(1)
else:
	print('Account: {}\r\nBalance: {}'.format(acc_info['data']['account'], acc_info['data']['balance']))

payments = ya.getHistory(records=3)	# Fetch 3 last payments
# Format: {'error': 1/0, ('error_message': '...',) 'data': dict('next_record': ..., 'operations': list(dict(), dict(), dict()... (Array with payments)))}
if payments['error']:
	print('Payments could not be fetched\r\nError: {}'.format(payments['error_message']))
	exit(1)
else:
	for payment in payments['data']['operations']:	# Display payment info (title, amount, direction (in/out))
		print('----------------------')
		print('Title: {}\r\nAmount: {}\r\nDirection: {}'.format(payment['title'], payment['amount'], payment['direction']))

# If you want to send a payment, use commented method below
# ya.makePayment('RECIEVER', AMOUNT, ('COMMENT'), to_phone=True(payment to a phone number associated with an acc/payment to an acc number))