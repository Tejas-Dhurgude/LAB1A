import requests
import matplotlib.pyplot as plt
from datetime import datetime

def get_etherscan_transactions(api_key, address, start_block=None, end_block=None):
    base_url = "https://api.etherscan.io/api"
    module = "account"
    action = "txlist"
    sort = "desc"
    params = {
        'apikey': api_key,
        'module': module,
        'action': action,
        'address': address,
        'sort': sort,
    }
    if start_block:
        params['startblock'] = start_block
    if end_block:
        params['endblock'] = end_block

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data['status'] == '1':
            transactions = data['result']
            return transactions
        else:
            print(f"Error: {data['message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def plot_transactions(transactions):
    if transactions:
        time_values = [datetime.fromtimestamp(int(tx['timeStamp'])) for tx in transactions]
        ether_values = [float(tx['value']) / 1e18 for tx in transactions]
        gas_values = [float(tx['gasPrice']) / 1e18 for tx in transactions]

        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(time_values, ether_values, marker='o', linestyle='-', color='b')
        plt.title('Account Time vs Ether(ETH) Value')
        plt.xlabel('Time')
        plt.ylabel('Ether(ETH) Value')

        plt.subplot(2, 1, 2)
        plt.plot(time_values, gas_values, marker='o', linestyle='-', color='r')
        plt.title('Account Time vs Gas paid (in ETH)')
        plt.xlabel('Time')
        plt.ylabel('Gas paid (ETH)')
        plt.tight_layout()
        plt.show()
    else:
        print("Error: Unable to fetch transactions.")

api_key = 'API-KEY'
user_address = '0x4976a4a02f38326660d17bf34b431dc6e2eb2327'
transactions = get_etherscan_transactions(api_key, user_address)

if transactions:
    print(f"Total transactions for {user_address}: {len(transactions)}")
    plot_transactions(transactions)
else:
    print("Error: Unable to fetch transactions.")
