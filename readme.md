# MTG Card Loader from Photo (WIP)

This is a work-in-progress project developed by my friends and me. Its goal is to help build a digital Magic: The Gathering card collection starting from photographs of physical cards.

### How It Works

The workflow is divided into three main steps:

1. **Card Detection**  
   The card is located within a photo using [OpenCV](https://opencv.org/).

2. **Information Extraction**  
   Key details from the area *below the text box* are extracted using [Keras](https://keras.io/). ([Learn more about this area](https://mtg.fandom.com/wiki/Information_below_the_text_box))

3. **Data Retrieval**  
   The extracted information is used to query [Scryfall](https://scryfall.com/), which returns complete card data.
