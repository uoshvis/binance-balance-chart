from binance.client import Client
import plotly.graph_objs as go
import plotly.offline as py

import config


def plot_pie(values, labels):
    # Plot pie chart

    total_BTC = sum(values)
    title = 'Estimated value: ' + str(total_BTC) + ' BTC'
    layout = go.Layout(title=title)
    trace = go.Pie(labels=labels, values=values)
    fig = go.Figure(data=[trace], layout=layout)
    py.plot(fig, filename='binance_balance_chart.html')


def main():
    client = Client(config.api_key, config.api_secret)

    # Get account information
    account = client.get_account()

    # Filter zero balances
    my_balance = {}
    for balance in account['balances']:
        if float(balance['free']) > 0:
            my_balance[balance['asset']] = {'free': float(balance['free'])}

    # Get current prices
    prices = client.get_all_tickers()

    # Add wallet data from config file
    '''
        wallet = {
            'symbol_1': amount,
            'symbol_2': amount
        }
    '''
    for k, v in config.wallet.items():
        if k in list(my_balance.keys()):
            my_balance[k]['free'] = my_balance[k]['free'] + v
        else:
            my_balance[k] = {}
            my_balance[k]['free'] = v

    # Filter only BTC prices by account assets and calculate total value
    for price in prices:
        symbol = price['symbol']
        if symbol[-3:] == 'BTC' and symbol[:-3] in list(my_balance.keys()):
            my_asset = my_balance[symbol[:-3]]
            my_asset['price'] = price['price']
            my_asset['value_BTC'] = (float(price['price']) * my_asset['free'])

    # Extract labels and values for chart
    labels = []
    values = []

    for key, value in my_balance.items():
        labels.append(key)
        if key == 'BTC':
            values.append(float(value['free']))
        else:
            values.append(value['value_BTC'])

    plot_pie(values, labels)

    # TODO add locked values to see reserved portion


if __name__ == '__main__':
    main()
