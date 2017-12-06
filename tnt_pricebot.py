#!/usr/bin/python3

import requests
import twitter
import argparse


options = argparse.ArgumentParser()
options.add_argument('--consumer-key', required=True)
options.add_argument('--consumer-secret', required=True)
options.add_argument('--token', required=True)
options.add_argument('--token-secret', required=True)


def get_tntprice():
    
    #Liqui
    r_liqui = requests.get('https://api.liqui.io/api/3/ticker/tnt_btc')
    json_liqui = r_liqui.json()
    liqui_sat = int(json_liqui['tnt_btc']['last']*10**8)
    
    r_liqui_usdt = requests.get('https://api.liqui.io/api/3/ticker/btc_usdt')
    json_liqui_usdt = r_liqui_usdt.json()
    liqui_usdt = "%.3f" % float(float(json_liqui_usdt['btc_usdt']['last'])*float(json_liqui['tnt_btc']['last']))
    
    liqui = 'Liqui:  ' + "%.8f" % float(liqui_sat/10**8) + ' BTC' + ' ($' + liqui_usdt + ')'

    #binance
    r_binance = requests.get('https://api.binance.com//api/v1/ticker/24hr?symbol=TNTBTC')
    json_binance = r_binance.json()
    binance_sat = int(float(json_binance['lastPrice'])*10**8)
    
    r_binance_usdt = requests.get('https://api.binance.com/api/v1/ticker/24hr?symbol=BTCUSDT')
    json_binance_usdt = r_binance_usdt.json()
    binance_usdt = "%.3f" % float(float(json_binance['lastPrice'])*float(json_binance_usdt['lastPrice']))
    
    binance = 'Binance:' + "%.8f" % float(binance_sat/10**8) + ' BTC' + ' ($' + binance_usdt + ')'

    #huobi
    r_huobi = requests.get('https://api.huobi.pro/market/trade?symbol=tntbtc')
    json_huobi = r_huobi.json()
    huobi_sat = int(float(json_huobi['tick']['data'][0]['price']*10**8))
    
    r_huobi_usdt = requests.get('https://api.huobi.pro/market/trade?symbol=btcusdt')
    json_huobi_usdt = r_huobi_usdt.json()
    huobi_usdt = "%.3f" % float(float(json_huobi_usdt['tick']['data'][0]['price'])*float(json_huobi['tick']['data'][0]['price']))
    
    huobi = 'Huobi:  ' + "%.8f" % float(huobi_sat/10**8) + ' BTC' + ' ($' + huobi_usdt + ')'
    
    tweet = 'Current prices of TNT are' + '\n' + '\n' + liqui + '\n' + binance + '\n' + huobi + '\n' + '\n' + '$TNT #Tierion'
    
    return tweet


def tweet_post(consumer_key, consumer_secret, token, token_secret, tweet):
    
    auth = twitter.OAuth(consumer_key=consumer_key,
                         consumer_secret=consumer_secret,
                         token=token,
                         token_secret=token_secret)

    t = twitter.Twitter(auth=auth)
    t.statuses.update(status=tweet) 

    
def main(opt):
    
    tweet = get_tntprice()
    tweet_post(consumer_key=opt.consumer_key, 
               consumer_secret=opt.consumer_secret, 
               token=opt.token, 
               token_secret=opt.token_secret, 
               tweet=tweet) 
    exit(0)
    

if __name__ == '__main__':
    main(options.parse_args())
    
