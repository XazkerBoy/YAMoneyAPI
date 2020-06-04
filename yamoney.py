import requests as r
import webbrowser
import json

class YandexMoney:
	client_id = None	# Client ID (register an app - get its token)
	headers = {"Content-Type": "application/x-www-form-urlencoded"}	# Headers
	api_url = 'https://money.yandex.ru'	# Main URL

	def __init__(self, client_id, token = None, redirect_url = None):
		if client_id is None:
			raise Exception("Client_ID not set") 
		self.client_id = client_id
		if token is None:	# No token given - get it
			if redirect_url is None:
				raise Exception("Redirect URL not set")
			token = self.getToken(client_id, redirect_url)
			if token['error']:
				raise Exception(token['error_message'])
			token = token['data']
			print('YOUR ACCESS TOKEN (valid for 3 years): {}'.format(token))
		self.headers['Authorization'] = "Bearer {}".format(token)	# Add authorization token to headers
error': 0 (No errors)/1 (An error occured), 'error_message': '...' (error message, only if an error occured)/'data': str/list(dict) (If no errors occured, response from the server/specified element will be returned)}
	def getToken(self, client_id, redirect_url):	# Get token using Client ID (Redirect URL MUST be the same as in the app description)
		if redirect_url is None:
			return {'error': 1, 'error_message': 'Redirect URL not set'}
		code_req = r.post(f'{self.api_url}/oauth/authorize', data=f'client_id={client_id}&response_type=code&redirect_uri={redirect_url}&scope=account-info operation-history payment-p2p operation-details', allow_redirects=False, headers=self.headers)
		webbrowser.open(code_req.headers.get('Location'), new=2)	# Open recieved URL and let user submit
		code = input('Token (after redirect in URL panel as parameter): ')	# After the user gets redirected, there will be a parameter 'code', which has to be put here
		token_req = r.post(f'{self.api_url}/oauth/token', data=f'code={code}&client_id={client_id}&grant_type=authorization_code&redirect_uri={redirect_url}', headers=self.headers)	# Fetch final toke using app ID and recieved temp-token
		if token_req.status_code is not 200:
			return {'error': 1, 'error_message': f'Status code: {token_req.status_code}'}
		return {'error': 0, 'data': token_req.json()['access_token']}

	def getAccInfo(self):	# Get account info (balance, payment methods...)
		if not 'Authorization' in self.headers.keys():
			return {'error': 1, 'error_message': 'Token not set'}
		acc = r.post(f'{self.api_url}/api/account-info', headers=self.headers)
		if acc.status_code is not 200:
			return {'error': 1, 'error_message': f'Status code: {acc.status_code}'}
		return {'error': 0, 'data': acc.json()}

	def getHistory(self, type=0, records=10):	# Get full details about specified amount of records (amount, comment, in/out...)
		if not 'Authorization' in self.headers.keys():
			return {'error': 1, 'error_message': 'Token not set'}
		oper_type = ''	# Fetch specified operations (empty for all; type = 1 - deposit; type = 2 - payment)
		if type is 1:
			oper_type = 'deposition'
		elif type is 2:
			oper_type = 'payment'
		payments = r.post(f'{self.api_url}/api/operation-history', data=f'type={oper_type}&records={records}&details=true', headers=self.headers)
		if payments.status_code is not 200:
			return {'error': 1, 'error_message': f'Status code: {payments.status_code}'}
		return {'error': 0, 'data': payments.json()}

	def makePayment(self, to, amount, comment='', to_phone=True):	# Make payment to account/phone associated with it (ThIs MeThOd WaS NoT TeStEd BeCaUsE I dOnT HavE aNy MoNeY)
		if not 'Authorization' in self.headers.keys():
			return {'error': 1, 'error_message': 'Token not set'}
		if to is None:
			return {'error': 1, 'error_message': 'Reciever not set'}
		if amount is None:
			return {'error': 1, 'error_message': 'Amount not set'}
		status = r.post(f'{self.api_url}/api/request-payment', data=f'pattern_id=p2p&to={to}' + ('&identifier_type=phone' if to_phone else '') + f'&amount={amount}&comment={comment}', headers=self.headers)	# Create a payment with user creds and amount
		if status.status_code is not 200:
			return {'error': 1, 'error_message': f'Status code: {status.status_code}'}
		status = status.json()
		if not status['wallet']['allowed']:	# Check if the payment is allowed (yandex checks, if there is enough balance)
			return {'error': 1, 'error_message': "Payments from wallet not allowed"}
		confirm = r.post(f'{self.api_url}/api/process-payment', data='request_id={}'.format(status['request_id']), headers=self.headers)	# Confirm payment
		if confirm.status_code is not 200:
			return {'error': 1, 'error_message': f'Status code: {confirm.status_code}'}
		return {'error': 0, 'data': confirm.json()}