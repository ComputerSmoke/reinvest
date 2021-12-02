from brownie import accounts, interface, network, config
from brownie.network import gas_price
import helper
import time
gas_price("60 gwei")
account = accounts.load("met")
maticAddress = "0x0000000000000000000000000000000000001010"
matic = interface.IERC20(maticAddress)
poolAddressProviderRegistry = interface.ILendingPoolAddressesProviderRegistry("0x3ac4e9aa29940770aeC38fe853a4bbabb2dA9C19")
poolAddressProvider = interface.ILendingPoolAddressesProvider(poolAddressProviderRegistry.getAddressesProvidersList()[0])
pool = interface.ILendingPool(poolAddressProvider.getLendingPool())
maticPriceAddress = "0x327e23A4855b6F663a28c5161541d69Af8973302"

def unstake(amount):
    return

def stake(amount):
    return

def repay(collateral, debt):
    maticPrice = helper.getAssetPrice(maticPriceAddress)
    toRepay = (debt / collateral - .5) * debt * maticPrice
    unstake(toRepay)#TODO

def borrow(collateral, debt):
    maticPrice = helper.getAssetPrice(maticPriceAddress)
    toBorrow = (.5 - debt / collateral) * debt * maticPrice
    print("Borrowing", toBorrow, " matic")
    tx = pool.borrow(
        maticAddress,
        toBorrow,
        2, 
        0,
        account,
        {"from": account}
    )
    tx.wait(1)
    stake()#TODO

def balanceHF():
    (collateral, debt,_,_,_,_) = pool.getUserAccountData()
    ltv = debt / collateral
    if ltv > .7:
        repay(collateral, debt)
    elif ltv < .3:
        borrow(collateral, debt)

def main():
    balanceHF()