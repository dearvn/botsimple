"""
Intergrate to cnbc

"""
import os, json, logging
import requests
import numpy as np

log = logging.getLogger(__name__)


def get_quota_cnbc_ticker(ticker):
    try:
        url = 'https://quote.cnbc.com/quote-html-webservice/quote.htm?symbols=' + ticker + '&requestMethod=quick&exthrs=1&noform=1&fund=1&output=json&events=1'
        r = requests.get(url)
        resp = r.json()
        if resp['QuickQuoteResult'] == None or resp['QuickQuoteResult']['QuickQuote'] == None:
            return None
        data = resp['QuickQuoteResult']['QuickQuote']

        data_watchlist = {'yrhipct':0}

        if "curmktstatus" in data and data['curmktstatus'] == 'REG_MKT':
            if 'last_time_msec' in data:
                data_watchlist['time'] = int(data['last_time_msec'])
            if 'change' in data:
                data_watchlist['change'] = float(data['change'])
            if 'change_pct' in data:
                data_watchlist['pct'] = float(data['change_pct'])
            if 'last' in data:
                data_watchlist['price'] = float(data['last'])
            if 'volume' in data:
                data_watchlist['volume'] = int(data['volume'])
        elif "ExtendedMktQuote" in data:
            if 'last_time_msec' in data['ExtendedMktQuote']:
                data_watchlist['time'] = int(data['ExtendedMktQuote']['last_time_msec'])
            if 'change' in data['ExtendedMktQuote']:
                data_watchlist['change'] = float(data['ExtendedMktQuote']['change'])
            if 'change_pct' in data['ExtendedMktQuote']:
                data_watchlist['pct'] = float(data['ExtendedMktQuote']['change_pct'])
            if 'last' in data['ExtendedMktQuote']:
                data_watchlist['price'] = float(data['ExtendedMktQuote']['last'])
            if 'volume' in data['ExtendedMktQuote']:
                data_watchlist['volume'] = int(data['ExtendedMktQuote']['volume'])
        if "FundamentalData" in data:
            mktcapView = data['FundamentalData']['mktcapView']
            if 'M' in mktcapView:
                mktcapView = float(mktcapView.replace('M', '')) * 1000000
            elif 'B' in mktcapView:
                mktcapView = float(mktcapView.replace('B', '')) * 1000000000
            data_watchlist['mktcap'] = mktcapView

            data_watchlist['yrhiprice'] = float(data['FundamentalData']['yrhiprice'])
            data_watchlist['yrloprice'] = float(data['FundamentalData']['yrloprice'])
            if 'price' in data_watchlist:
                data_watchlist['yrhipct'] = (data_watchlist['price']/data_watchlist['yrhiprice']) * 100

        return data_watchlist

    except AssertionError as e:
        log.exception(e)
    except Exception as e:
        log.exception(e)


def post_quota_cnbc_ticker(ticker):
    try:
        item = get_quota_cnbc_ticker(ticker)

        if item == None:
            return
        body = {}
        body[ticker] = item
        # post back to site
        url = os.environ.get('API_URI') + "/api/quota-ticker"
        headers = {'content-type': 'application/json',
                   'accept': 'application/json',
                   'authorization': os.environ.get('API_KEY')}
        data = json.dumps(body, cls=NpEncoder)
        resp = requests.post(url=url, data=data, headers=headers)

    except AssertionError as e:
        log.exception(e)
    except Exception as e:
        log.exception(e)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.bool_)):
            return int(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
