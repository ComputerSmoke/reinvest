from brownie import accounts, interface, network, config
from brownie.network import gas_price
import time
gas_price("60 gwei")
account = accounts.load("met")
kiroAddress = "0xB382C1cfA622795a534e5bd56Fac93d59BAc8B0D"
kiro = interface.IERC20(kiroAddress)
wmaticAddress = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
wmatic = interface.IERC20(wmaticAddress)
routerAddress = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"
router = interface.IUniswapV2Router02(routerAddress)
rewardsAddress = "0xfF22Bf1f778BcD6741D823b077285533EC582F78"
rewards = interface.IStakingDualRewards(rewardsAddress)
uv2Address = "0x3f245C6f18442Bd6198d964C567a01BD4202e290"
uv2 = interface.IERC20(uv2Address)

def reinvestKIRO():
    #get rewards
    getRewards()
    #Swap half our KIRO to WMATIC
    swapKiro()
    #Add our KIRO/MATIC liquidity
    addLiquidity()
    #Stake amount
    stake()

def stake():
    liquidity = uv2.balanceOf(account, {"from":account})
    print("Staking " + str(liquidity) + " liquidity")
    rewards.stake(liquidity, {"from": account})

def getDeadline():
    return int(time.time() + 900)

def addLiquidity():
    kiroOwned = kiro.balanceOf(account, {"from": account})
    wmaticOwned = wmatic.balanceOf(account, {"from": account})
    rate = kiroOwned / router.getAmountOut(kiroOwned, kiroAddress, wmaticAddress, {"from": account})
    kiroMin = wmaticOwned * rate * 0.99
    wmaticMin = kiroOwned / rate * 0.99
    router.addLiquidity(kiroAddress, wmaticAddress, kiroOwned, wmaticOwned, kiroMin, wmaticMin, account, getDeadline(), {"from": account})
    print("Added liquidity")


def swapKiro():
    kiroOwned = kiro.balanceOf(account, {"from": account})
    print("Swapping " + str(kiroOwned/2) + " KIRO to WMATIC")
    min = router.getAmountOut(int(kiroOwned/2), kiroAddress, wmaticAddress, {"from": account}) * .99
    router.swapExactTokensForTokens(kiroOwned/2, min, [kiroAddress, wmaticAddress], account, getDeadline(), {"from": account})
    

def getRewards():
    earnedA = rewards.earnedA(account, {"from": account})
    earnedB = rewards.earnedB(account, {"from": account})
    print("Withdrawing A: " + str(earnedA) + ", B: " + str(earnedB))
    rewards.getReward({"from": account})


def main():
    reinvestKIRO()