import requests
from datetime import datetime


def get_amda_token(base_url="http://amda.irap.omp.eu"):
    return requests.get(f"{base_url}/php/rest/auth.php?").text


def get_amda_dl_url(product='thb_bl', start_time=datetime(2018, 10, 14, 0), stop_time=datetime(2018, 10, 14, 10),
                    token=None, base_url="http://amda.irap.omp.eu", output_format="ASCII", debug=False):
    if token is None:
        token = get_amda_token(base_url)
    if type(start_time) is datetime:
        start_time = start_time.timestamp()
    if type(stop_time) is datetime:
        stop_time = stop_time.timestamp()
    url = f"{base_url}/php/rest/getParameter.php?parameterID={product}&startTime={start_time}&stopTime={stop_time}&timeFormat='UNIXTIME'&outputFormat={output_format}&token={token}"
    if debug:
        print(url)
    resp = requests.get(url)
    js = resp.json()
    if 'success' in js and js['success'] is True and 'dataFileURLs' in js:
        if debug:
            print(js['dataFileURLs'])
        return js['dataFileURLs']
    else:
        print(js)
        return None


def get_from_amda(product='thb_bl', start_time=datetime(2018, 10, 14, 0), stop_time=datetime(2018, 10, 14, 6),
                  token=None, base_url="http://amda.irap.omp.eu", output_format="ASCII", debug=False):
    data = requests.get(
        get_amda_dl_url(product=product, start_time=start_time, stop_time=stop_time, token=token, base_url=base_url,
                        output_format=output_format,
                        debug=debug))
    return data.content if data is not None else None


def dl_from_rest_api(output_format="ASCII"):
    return get_from_amda(output_format=output_format)
