import requests
import json

RPC_URL = "https://api.mainnet-beta.solana.com"

def get_token_supply(token_mint):
    """
    Fetches token supply information for a given token mint using the
    Solana JSON RPC API's getTokenSupply method.
    
    :param token_mint: The token mint address.
    :return: A dictionary with the token supply information, or None if an error occurs.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenSupply",
        "params": [token_mint]
    }
    
    try:
        response = requests.post(RPC_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("result", {})
        else:
            print("Error fetching token supply:", response.status_code)
            return None
    except Exception as e:
        print("Exception in get_token_supply:", e)
        return None

def get_token_holders(token_mint):
    """
    Fetches the token accounts by mint to determine the number of holders.
    Uses the Solana JSON RPC API's getTokenAccountsByMint method.
    
    :param token_mint: The token mint address.
    :return: The number of token holders (unique accounts), or None if an error occurs.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByMint",
        "params": [
            token_mint,
            {"encoding": "jsonParsed"}
        ]
    }
    
    try:
        response = requests.post(RPC_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            accounts = data.get("result", {}).get("value", [])
            return len(accounts)
        else:
            print("Error fetching token holders:", response.status_code)
            return None
    except Exception as e:
        print("Exception in get_token_holders:", e)
        return None

def get_token_metadata(token_mint):
    """
    Combines token supply and holder count to form a metadata dictionary
    similar to what the Solscan API might return.
    
    :param token_mint: The token mint address.
    :return: A dictionary containing token supply information and holder count.
    """
    supply_info = get_token_supply(token_mint)
    holder_count = get_token_holders(token_mint)
    metadata = {
        "supply_info": supply_info,
        "holder_count": holder_count
    }
    return metadata

# --- Example Usage ---
if __name__ == '__main__':
    # Replace with a valid token mint address on Solana
    token_mint_address = "4zK39MUeEzpHWCTQjNXqfnUd7MvcciByjWG2ByBwpump"
    
    metadata = get_token_metadata(token_mint_address)
    if metadata:
        print("Fetched Token Metadata:")
        print(json.dumps(metadata, indent=4))
    else:
        print("No token metadata available.")
