from flask import Flask, request
from stellar_sdk import Server, xdr
import stellar_sdk.server
from stellar_sdk.operation import manage_buy_offer
from stellar_sdk.operation.manage_sell_offer import ManageSellOffer
from waitress import serve
import stellar_sdk
from stellar_sdk import Asset
from stellar_sdk import Account, Keypair, Network, TransactionBuilder
from stellar_sdk import Operation
import sched, time
import json
import math

# Variables

# Native Asset vs USDC is the default (and only) configuration so far.
native = Asset.native()
usdc = Asset("USDC", "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN")
size = 0
xlmPrice = 0
#Input these in "secret.txt" file as described
secret = ""
coinAPIKey = ""

i=0
f=open('secret.txt')
for line in f:
    if(i == 0):
        secret = line
    if(i == 1):
        coinAPIKey = line
    i+=1

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

root_keypair = Keypair.from_secret(secret)
public_key = root_keypair.public_key
network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
server = Server(horizon_url="https://horizon.stellar.org")
fee = server.fetch_base_fee()
app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)

def renewPrice():
    import requests
    url = 'https://rest.coinapi.io/v1/exchangerate/XLM/USD'
    headers = {'X-CoinAPI-Key' : coinAPIKey}
    xlmPriceresponse = requests.get(url, headers=headers)
    xlmjsonPrice = xlmPriceresponse.json()
    xlmjsPrice = json.dumps(xlmjsonPrice)
    xlmPrice = json.loads(xlmjsPrice)
    xlmPrice = xlmPrice['rate']
    print("got new price: " + str(xlmPrice))

renewPrice()

#buy USDC
@app.route('/trade/buy', methods=['POST'])
def result():
    size = request.args['size']
    print("SIZING IS: " + str(float(size)))
    print("XLM PRICE IS: " + str(xlmPrice - float(str(0.1))))
    transaction = manage_buy_offer.ManageBuyOffer(native, usdc, str(float(size)), str(10.01))
    srcacc = server.load_account(account_id=root_keypair.public_key)

    sell_offer_transaction = (
    TransactionBuilder(
        source_account=srcacc,
        network_passphrase=network_passphrase,
        base_fee=fee,
    )
    .append_operation(transaction)
    .build()
)
    sell_offer_transaction.sign(root_keypair.secret)
    response = Server.submit_transaction(server, sell_offer_transaction)
    return 'Sold: '+ str(response)

#sell USDC
@app.route('/trade/sell', methods=['POST'])
def result2():
    size = request.args['size']

    transaction = manage_buy_offer.ManageBuyOffer(usdc, native, str(truncate(float(float(size) / xlmPrice), 5)), str(xlmPrice + 0.1))
    srcacc = server.load_account(account_id=root_keypair.public_key)

    sell_offer_transaction = (
    TransactionBuilder(
        source_account=srcacc,
        network_passphrase=network_passphrase,
        base_fee=fee,
    )
    .append_operation(transaction)
    .build()
)
    sell_offer_transaction.sign(root_keypair.secret)
    response = Server.submit_transaction(server, sell_offer_transaction)
    return 'Sold: '+ str(response)

serve(app, listen='*:80')