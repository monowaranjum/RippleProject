'''
This file contains the code for collecting the data by calling the
Ripple api and then uses those data to format edges and then dumps them into the database.

For the purpose of this course, we will be using sqlite.
In real world scenarios, the neo4j graphDB or some other implementations of robust DB is preferred
'''
import time
import requests
import dbhelper


def construct_queries(_marker=None):
    # This function constructs a request by using the following quesry parameters and send them to Ripple server to get the data.
    limit = "100"
    start = "2020-08-03T05:26:10"
    end = "2020-08-15T00:00:00"
    query_type = "Payment"

    base_url: str = "https://data.ripple.com/v2/transactions?"

    formatted_url = base_url
    if query_type != "":
        query_param_type = "type={0}".format(query_type)
        formatted_url = formatted_url + query_param_type
    if limit != "":
        query_param_limit = "&limit={0}".format(limit)
        formatted_url = formatted_url + query_param_limit
    if start != "":
        query_param_start = "&start={0}".format(start)
        formatted_url = formatted_url + query_param_start
    if end != "":
        query_param_end = "&end={0}".format(end)
        formatted_url = formatted_url + query_param_end
    if _marker is not None:
        query_param_marker = "&marker={0}".format(_marker)
        formatted_url = formatted_url + query_param_marker

    return formatted_url


def get_data(request_url):
    # This function reads the responds from the server and formats it
    response = requests.get(request_url)

    if response.status_code == 200:
        print("Success in fetching the data.")
    else:
        print("Failure in fetching the data. Response code: ", response.status_code)

    response_body = response.json()
    count = response_body['count']
    if 'marker' in response_body:
        marker = response_body['marker']
    else:
        marker = ""

    tx_list = response_body['transactions']
    obj_list = []
    for tx in tx_list:
        _hash = tx['hash']
        _time = tx['date']
        _type = tx['tx']['TransactionType']

        if isinstance(tx['tx']['Amount'], str):
            _a_val = float(tx['tx']['Amount'])
            _a_curr = 'XRP'
        elif isinstance(tx['tx']['Amount'], dict):
            _a_val = float(tx['tx']['Amount']['value'])
            _a_curr = tx['tx']['Amount']['currency']
        else:
            print('Unknown type found')
            pass

        _t_res = tx['meta']['TransactionResult']

        if _t_res == 'tesSUCCESS':
            if isinstance(tx['meta']['delivered_amount'], str):
                _d_val = float(tx['meta']['delivered_amount'])
                _d_curr = 'XRP'
            elif isinstance(tx['meta']['delivered_amount'], dict):
                _d_val = float(tx['meta']['delivered_amount']['value'])
                _d_curr = tx['meta']['delivered_amount']['currency']
        else:
            _d_val = 0.0
            _d_curr = "None"

        _accnt = tx['tx']['Account']
        _dest = tx['tx']['Destination']

        t_obj = dbhelper.TransactionObject(_hash, _time, _a_val, _a_curr, _t_res,
                                           _d_val, _d_curr, _accnt, _dest)
        obj_list.append(t_obj)

    return obj_list, marker


if __name__ == '__main__':
    query = construct_queries()
    o_li, next_marker = get_data(query)
    dbhelper.add_tx_obj(o_li)

    prev_marker = ""
    count = 0

    while True:
        if prev_marker == next_marker:
            break
        prev_marker = next_marker

        query = construct_queries(next_marker)
        o_li, next_marker = get_data(query)
        dbhelper.add_tx_obj(o_li)

        count += 1
        print('Request Count: ', count)
        if count % 100 == 0:
            time.sleep(300)
        elif count % 20 == 0:
            time.sleep(30)
