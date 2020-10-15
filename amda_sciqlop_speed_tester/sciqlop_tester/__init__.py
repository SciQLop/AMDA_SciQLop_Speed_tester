import requests
from datetime import datetime
import pickle


def get_from_proxy(product='thb_bl', start_time='2018-10-14%2000:00:00', stop_time='2018-10-14%2006:00:00',server="http://sciqlop.lpp.polytechnique.fr/cache"):
    if type(start_time) is datetime:
        start_time = start_time.isoformat()
    if type(stop_time) is datetime:
        stop_time = stop_time.isoformat()
    resp=requests.get(f"{server}/get_data?path=amda/{product}&start_time={start_time}&stop_time={stop_time}")
    return pickle.loads(resp.content)


def dl_from_rest_api():
    return get_from_proxy()