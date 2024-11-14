import requests

Verbose = False

# Endpoint used to access Scryfall database
BASE_URL = "https://api.scryfall.com/cards"

def card_search_one_by_one(collector_number, set_name):
    """
    Parameters
    ----------
    collector_number : specific number of the selected card
    set_name : abbreviation of the name of the set the card belongs to
    - - -
    - collector numbers and set names must have the same order (coupled for the same cards)
    - Returns a list of tuples containing name and expansion for each card
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
                print(f"Couldn't formulate the search for number = {num}, set = {exp};\nFollowing error has occourred: {e}")
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

def chunk_lists(chunk_size, data):
    """
    Parameters
    ----------
    chunk_size : size of the chunks to be generated
    data : list of tuples containing info of the cards, e.g.: [(name,set),(name2, set2)]
    - - -
    - Returns a list containing the chunks of the givern data with the given size
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]

def card_search_batch(collector_numbers, set_names):
    """
    Parameters
    ----------
    collector_numbers : list of collector numbers for all the cards requested
    set_name : abbreviations of the names of the sets the cards belongs to
    - - -
    - collector numbers and set names must have the same order (coupled for the same cards)
    - Returns a list of tuples containing name and expansion for each card
    """
    url = f"{BASE_URL}/collection"
    
    results = [] # Here we will store all results

    clean_params = []
    # Convert input into strings if possible
    for i in range(len(collector_numbers)):
        try:
            clean_params.append((str(collector_numbers[i]),str(set_names[i])))
        except Exception as e:
            if Verbose:
                print(f"Couldn't formulate the search for number = {collector_numbers[i]}, set = {set_names[i]};\nFollowing error has occourred: {e}")
            continue # ignore this card

    for chunk in chunk_lists(75, clean_params):
        identifiers = [{"collector_number":data[0], "set":data[1]} for data in chunk]
        response = requests.post(url, json={"identifiers": identifiers})

        if response.status_code == 200: # The research succeded
            cards = response.json().get("data", []) # access to current card
            for card in cards:
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
            continue
    return results


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# Example usage
if __name__ == "__main__":

    # Let's find the original Dreadmaw!
    coll_num = [180]
    exp = ['XLN']
    res = card_search_one_by_one(coll_num, exp)

   # Try out the search with more than one card
    coll_nums = [125,197,17]
    exps = ['RIX','AFR','BFZ']
    res = card_search_one_by_one(coll_nums, exps)

    # Here we try the batch search
    res = card_search_batch(coll_nums, exps)

    # Now let's try with more than 75 requests with the batch search
    for i in range(123):
        coll_nums.append('125')
        exps.append('RIX')
    res = card_search_batch(coll_nums, exps)