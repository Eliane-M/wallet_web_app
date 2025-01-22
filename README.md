# wallet_web_app

This is a web app for Eric to assist him with tracking his transactions and ensuring he does not miss any.
This directory is for the backend, developed using Django framework.

## Getting started

To get started with the website, you can use the [Live frontend website](https://wallet-web-app-hama.onrender.com). [Link for deployed backend](https://wallet-web-application-zzq9.onrender.com)
or clone the repo to use it locally. (Recommended in case the frontend link is giving trouble).

To clone the repo, use the following commands in your terminal

```
git clone https://github.com/Eliane-M/wallet_web_app.git
```
```
cd wallet_web_app
```

create a virtual environment
```
python -m venv venv
```

activate the virtual environment
```
source venv/Source/activate
```

install packages
```
pip install -r requirements.txt
```
then run the project on the local server
```
python manage.py runserver
```

## Below is a list of the URLs in the wallet_web_app:

### For authentication
To register/signup: http://127.0.0.1:8000/api/auth/register/

  Body:
  
    - email
    - password
    - full_name

To login: http://127.0.0.1:8000/api/auth/login/

  Body:
  
    - username (use the registered email)
    - password

### For Transactions
To get all transactions: http://127.0.0.1:8000/api/wallet/

To get the current balance: http://127.0.0.1:8000/api/wallet/balance/

To withdraw: http://127.0.0.1:8000/api/wallet/withdraw/

  Body:
  
    - transaction_type: "Withdrawal"
    - amount

To deposit: http://127.0.0.1:8000/api/wallet/deposit/

  Body:
  
    - transaction_type: "Deposit"
    - amount

To get a report: http://127.0.0.1:8000/api/wallet/report/

  Body:
  
    - start_date: "MM/DD/YYYY"
    - end_date: "MM/DD/YY"
    - account_id
    - report_format (default=csv)

### For account creations
http://127.0.0.1:8000/api/accounts/

  Body:
  
    - name
    - account_type (can either be momo_account, bank_account or cash)
    if the account type is momo_account:
      - phone_number
      - provider (ex: MTN)

    if the account type is bank_account:
      - account_number
      - bank_name
      - account_holder_name

    if account_type is cash:
      no body

All 'GET' requests don't need a body
