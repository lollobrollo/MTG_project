import scryfall_requests as scr

def csv_encoder(search_results):
    """
    Parameters
    ----------
    search_results : list of tuples (name, expansion, language) for all the cards
    - - -
    - This function generates a .csv file compatible whith ManaBox to be imported in a collection
    """
    with open('cards.csv','w+') as file:
        header = "set,lang,name"
        file.write(header + "\n")
        for row in search_results:
            file.write(','.join(row) + '\n')
    print(f"Data written to {file_path}")
