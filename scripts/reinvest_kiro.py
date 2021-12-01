from brownie import accounts, interface, network, config
import time

def reinvestKIRO():
    account = accounts.load("met")
    kiroAddress = "0xb1191f691a355b43542bea9b8847bc73e7abb137"
    kiro = interface.IERC20(kiroAddress)
    wmaticAddress = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
    wmatic = interface.IERC20(wmaticAddress)
    routerAddress = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"
    router = interface.IUniswapV2Router02(routerAddress)
    rewardsAddress = "0xfF22Bf1f778BcD6741D823b077285533EC582F78"
    rewards = interface.StakingDualRewards(rewardsAddress)
    #get rewards
    getRewards(account, rewards)
    #Swap half our KIRO to WMATIC
    swapKiro(account, kiroAddress, wmaticAddress, router, kiro)
    #Add our KIRO/MATIC liquidity
    liquidity = addLiquidity(account, kiroAddress, wmaticAddress, kiro, wmatic, router)
    #Stake amount
    stake(account, rewards, liquidity)

def stake(account, rewards, liquidity):
    rewards.stake(liquidity, {"from": account})

def getDeadline():
    return int(time.time() + 900)

def addLiquidity(account, kiroAddress, wmaticAddress, kiro, wmatic, router):
    kiroOwned = kiro.balanceOf(account, {"from": account})
    wmaticOwned = wmatic.balanceOf(account, {"from": account})
    rate = kiroOwned / router.getAmountOut(kiroOwned, kiroAddress, wmaticAddress, {"from": account})
    kiroMin = wmaticOwned * rate * 0.99
    wmaticMin = kiroOwned / rate * 0.99
    (_,_,liquidity) = router.addLiquidity(
        kiroAddress, wmaticAddress, kiroOwned, wmaticOwned, kiroMin, wmaticMin, account, getDeadline(), {"from": account})
    return liquidity


def swapKiro(account, kiroAddress, wmaticAddress, router, kiro):
    kiroOwned = kiro.balanceOf(account, {"from": account})
    print("Swapping " + str(kiroOwned/2) + " KIRO to WMATIC")
    min = router.getAmountOut(int(kiroOwned/2), kiroAddress, wmaticAddress, {"from": account}) * .99
    router.swapExactTokensForTokens(kiroOwned/2, min, [kiroAddress, wmaticAddress], account, getDeadline(), {"from": account})
    

def getRewards(account, rewards):
    earnedA = rewards.earnedA(account, {"from": account})
    earnedB = rewards.earnedB(account, {"from": account})
    print("Withdrew A: " + str(earnedA) + ", B: " + str(earnedB))
    rewards.getReward({"from": account})


def main():
    #reinvestKIRO()
    return