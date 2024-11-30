import scryfall_requests as scr

file_path = "Data\\cards.csv"

def csv_encoder(search_results):
    """
    Parameters
    ----------
    search_results : list of tuples (name, expansion, language) for all the cards
    - - -
    - This function generates a .csv file compatible whith ManaBox to be imported in a collection
    """
    with open(file_path,'w+') as file:
        header = "set,lang,name"
        file.write(header + "\n")
        for row in search_results:
            file.write('"' + '","'.join(row) + '"' + '\n')
    print(f"Data written to {file_path}")


# Time for some checks
if __name__ == "__main__":
    
    coll_nums = [125,197,35]
    exps = ['RIX','AFR','ltc']
    langs = ['EN','IT','EN']
    res = scr.card_search_batch(coll_nums, exps, langs)
    csv_encoder(res)