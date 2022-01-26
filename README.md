# stellar-tradingview-server
Quick TradingView Server for buying/selling XLM/USDC on Stellar Network

This is a quick example/demo of a server that was tested on Ubuntu CLI system to accept TradingView "Webhook notifications" calls.

Note that you would need Pro (or any other paid) Subscription from tradingview at the moment to use Webhook feature.

If you were to use this, you'd have to input your XLM secret into first line of "secret.txt" and a free API key off https://docs.coinapi.io/#md-docs in second line (press enter to make sure it's on second line, etc)

Then, call relevant function, like ServerIp/trade/sell?size=10 (to sell 10 USD worth) from webhook URL when you set up a TradingView notification.

That's mostly it, whole thing consists of single .py file, so check out imports to make sure you "pip install" any missing components.

Even though I didn't expect anyone to need this as I put it out as personal demo, I'd still like to put out generic legal warning:

This project is for informational purposes only. You should not construe any such information or other material as legal, tax, investment, financial, or other advice. Nothing contained here constitutes a solicitation, recommendation, endorsement, or offer by me or any third party service provider to buy or sell any securities or other financial instruments in this or in any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such jurisdiction.

If you plan to use real money, USE AT YOUR OWN RISK.

Under no circumstances will I be held responsible or liable in any way for any claims, damages, losses, expenses, costs, or liabilities whatsoever, including, without limitation, any direct or indirect damages for loss of profits.


