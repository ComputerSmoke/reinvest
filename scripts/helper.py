from brownie import interface

def getAssetPrice(price_feed_address):
    price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = price_feed.latestRoundData()[1]
    return latest_price