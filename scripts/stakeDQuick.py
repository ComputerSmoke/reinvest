from brownie import accounts, interface, network, config
from brownie.network import gas_price
import time
gas_price("60 gwei")
account = accounts.load("met")

dQuickAddress = "0xf28164A485B0B2C90639E47b0f377b4a438a16B1"
dQuick = interface.IERC20(dQuickAddress)

def stakeDQuick():
    return#TODO

def main():
    stakeDQuick()