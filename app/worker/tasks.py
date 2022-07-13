from __future__ import absolute_import
import logging

from .worker import app

from .cnbc import post_quota_cnbc_ticker
logger = logging.getLogger(__name__)

@app.task(bind=True, name='get_quote_exe', default_retry_delay=10)
def get_quote_exe(self, ticker):
    try:
        post_quota_cnbc_ticker(ticker)

    except Exception as exc:
        raise self.retry(exc=exc)
