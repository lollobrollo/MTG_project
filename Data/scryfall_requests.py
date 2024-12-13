import requests

# Set True to see some more info during runtime
Verbose = True

# Endpoint used to access Scryfall database
BASE_URL = "https://api.scryfall.com/cards"

def card_search_one_by_one(collector_number, set_name, lang):
    """
    Parameters
    ----------
    collector_number : list of collector numbers for all the cards requested
    set_name : abbreviations of the names of the sets the cards belongs to
    lang : list containing the languages of the cards
    These three lists must have the same order (same index -> same card)
    - - -
    - Returns a list of tuples containing name and expansion for each card
    """

    url = f"{BASE_URL}/search"
    
    results = [] # Here we will store all results

    # Do the following for each card searched
    for i in range(len(collector_number)):
        # Ceck if I can convert input into strings and build a query using scryfall's search syntax
        try:
            query = f"cn:{str(collector_number[i])} s:{str(set_name[i])}"
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
            results.append((card['name'], card['set_name'], lang[i]))
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

def card_search_batch(collector_number, set_name, lang):
    """
    Parameters
    ----------
    collector_number : list of collector numbers for all the cards requested
    set_name : abbreviations of the names of the sets the cards belongs to
    lang : list containing the languages of the cards
    - These three lists must have the same order (same index -> same card)
    - - -
    - Returns a list of tuples containing name and expansion for each card
    """
    url = f"{BASE_URL}/collection"
    
    results = [] # Here we will store all results
    deleted = [0 for _ in range(len(collector_number))] # Used to later update language vector

    clean_params = []
    # Convert input into strings if possible
    for i in range(len(collector_number)):
        try:
            clean_params.append((str(collector_number[i]),str(set_name[i])))
            lang[i] = str(lang[i])
        except Exception as e:
            if Verbose:
                print(f"Couldn't formulate the search for number = {collector_number[i]}, set = {set_name[i]}, language = {lang[i]};\nFollowing error has occourred: {e}")
            deleted[i] = 1
            continue # ignore this card

    # Update languages list deleting unused cards
    lang = [lang[i] for i in range(len(lang)) if deleted[i] == 0]

    for  chunk in chunk_lists(75, clean_params):
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

    return [(str(r[0]), str(r[1]), str(l)) for r, l in zip(results, lang)]


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# Example usage
if __name__ == "__main__":

    # Let's find the original Dreadmaw!
    coll_num = [180]
    exp = ['XLN']
    lang = ['EN']
    card_search_one_by_one(coll_num, exp, lang)

   # Try out the search with more than one card (and an error in the input)
    coll_nums = [125,197,17]
    exps = ['RIX','AFR','BF']
    langs = ['EN','IT','EN']
    res = card_search_one_by_one(coll_nums, exps, langs)
    print(res)

    # Here we try the batch search
    coll_nums = [125,197,17]
    exps = ['RIX','AFR','mid']
    langs = ['EN','IT','EN']
    res = card_search_batch(coll_nums, exps, langs)
    print(res)

    # Now let's try with more than 75 requests with the batch search
    for i in range(75):
        coll_nums.append('125')
        exps.append('RIX')
        langs.append('EN')
    card_search_batch(coll_nums, exps, langs)