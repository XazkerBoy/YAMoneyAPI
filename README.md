# YAMoneyAPI-PY
Class with basic Yandex.Money API functions (get token, get account info / payments, send payment)

# Usage
1. Import class
```python
from yamoney import YandexMoney
```
2.1. If you do not have a permanent token, use this method (but before, [Register an app](https://money.yandex.ru/myservices/new.xml))
```python
ya = YandexMoney("YOUR_CLIENT_ID", redirect_url="URL_SET_IN_REGISTRATION")
```
> (this init will create and open a confirmation link, where you have to confirm token creation and use the code after redirect to generate permenent token)

2.2. If you already have a token, use this one
```python
ya = YandexMoney("YOUR_CLIENT_ID", "YOUR_TOKEN")
```
3. After the init use any of the methods below
# Methods

Name|Parameters|Description
--- | --- | ---
**getAccInfo()**||Get account information (balance, ID...)
**getHistory()**|type = 0 (1 - in; 2 - out), records = 10 (No. of records)|Get payment history of specified amount of records and specified type (in/out)
**makePayment()**|to, amount, comment = '', to_phone = True (True - to phone; False - to ID)|Make a pamyent to specified user ID/phone

> Each method returns response with following structure:

> {'error': 0 (No errors)/1 (An error occured), 'error_message': '...' (error message, only if an error occured)/'data': str/list(dict) (If no errors occured, response from the server/specified element will be returned)}
