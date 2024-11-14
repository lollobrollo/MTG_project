import requests

Verbose = True
# Endpoint used to access Scryfall database
BASE_URL = "https://api.scryfall.com/cards"

def card_search(collector_number, set_name):
    """
    Parameters
    ----------
    collector_number : specific number of the selected card
    set_name : abbreviation of the name of the set the card belongs to
    Returns : list of tuples containing name and expansion for each card
    """
    url = f"{BASE_URL}/search"

    results = [] # Here we will store all results

    # Do the following for each card searched
    for num, exp in zip(collector_number, set_name):
        # Ceck if I can convert input into strings and build a query using scryfall's search syntax
        try:
            query = f"cn:{str(num)} s:{str(exp)}"
        except Exception as e:
            if Verbose:
                print(f"Couldn't formulate the search for number = {num}, set = {exp};\nError occourred: {e}")
            continue # ignore this card

        # Build the request for the API
        params = {
            "q": query,
            "unique": "cards", # Remove duplicates
            "order": "released", # Type of ordering
            "dir": "asc" # Direction of ordering
        }
        response = requests.get(url, params=params)

        if response.status_code == 200: # The research succeded
            card = response.json().get("data", [])[0] # access to current card
            results.append((card['name'], card['set_name']))
            if Verbose:
                print(f"Name: {card['name']}")
                print(f"Type: {card['type_line']}")
                print(f"Set Name: {card['set_name']}")
                print(f"Rarity: {card['rarity']}")
                print("-" * 20)
        else:
            if Verbose:
                print(f"Error: {response.status_code} - {response.json().get('details', 'No details')}")
            pass
    return results


# Example usage
if __name__ == "__main__":

    # Let's find the original Dreadmaw!
    coll_num = [180]
    exp = ['XLN']
    res = card_search(coll_num, exp)

   # Try out the search with more than one card
    coll_nums = [125,197,17]
    exps = ['RIX','AFR','BFZ']
    res = card_search(coll_nums, exps)