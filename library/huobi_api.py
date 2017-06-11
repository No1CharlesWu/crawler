from library.huobi_util import *

API_KEY = 'd9cf78de-f6da672b-52911e2c-b064c'
SECRET_KEY = '03ff8324-f6092b49-b370309f-2cff5'

TICKER_BTC_CNY = 'http://api.huobi.com/staticmarket/ticker_btc_json.js'
TICKER_LTC_CNY = 'http://api.huobi.com/staticmarket/ticker_ltc_json.js'
TICKER_BTC_USD = 'http://api.huobi.com/usdmarket/ticker_btc_json.js'

DEPTH_BTC_CNY = 'http://api.huobi.com/staticmarket/depth_btc_json.js'
DEPTH_LTC_CNY = 'http://api.huobi.com/staticmarket/depth_ltc_json.js'
DEPTH_BTC_USD = 'http://api.huobi.com/usdmarket/depth_btc_json.js'

KLINE_BTC_CNY = 'http://api.huobi.com/staticmarket/btc_kline_[period]_json.js'
KLINE_LTC_CNY = 'http://api.huobi.com/staticmarket/ltc_kline_[period]_json.js'
KLINE_BTC_USD = 'http://api.huobi.com/usdmarket/btc_kline_[period]_json.js'

DETAIL_BTC_CNY= 'http://api.huobi.com/staticmarket/detail_btc_json.js'
DETAIL_LTC_CNY= 'http://api.huobi.com/staticmarket/detail_ltc_json.js'
DETAIL_BTC_USD= 'http://api.huobi.com/usdmarket/detail_btc_json.js'

class HuobiSpot(object):
    def __init__(self, api_key, secret_key):
        self.__api_key = api_key
        self.__secret_key = secret_key

    def get_ticker(self, url):
        return httpRequest(url, {})

    def get_depth(self, url, count=150):
        if not isinstance(count, int) or count > 150 or count < 0:
            print('error: get_depth params error.')
            return None

        if count < 150 and count > 0:
            url = url.replace('json', str(count))
        return httpRequest(url, {})

    def get_kline(self, url, period, length=300):
        l = ['001', '005', '015', '030', '060', '100', '200', '300', '400']
        if period not in l:
            print('error: get_kline period error.')
            return None
        if not isinstance(length, int) or length > 2000 or length < 0:
            print('error: get_kline length error.')
            return None

        url = url.replace('[period]', period)
        url = url + '?' + 'length' + '=' + str(length)
        return httpRequest(url, {})

    def get_detail(self, url):
        return httpRequest(url, {})

if __name__ == '__main__':
    a = HuobiSpot('1', '2')
    # r = a.get_depth(DEPTH_BTC_CNY)
    # r = a.get_ticker(TICKER_BTC_CNY)
    # print(r)
    # count = 0
    # for i in r['bids']:
    #     count += 1
    #     print(count, i)
    # r = a.get_depth(DEPTH_BTC_CNY, 2)
    # r = a.get_ticker(TICKER_BTC_CNY)
    # r = a.get_kline(KLINE_BTC_CNY, '001', 10)
    r = a.get_detail(DETAIL_BTC_CNY)
    print(type(r), r)
