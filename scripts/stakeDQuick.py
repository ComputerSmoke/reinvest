from brownie import accounts, interface, network, config
from brownie.network import gas_price
import time
gas_price("60 gwei")
account = accounts.load("met")

dQuickAddress = "0xf28164A485B0B2C90639E47b0f377b4a438a16B1"
dQuick = interface.IERC20(dQuickAddress)
rewardsAddress = "0xa751f7B39F6c111d10e2C603bE2a12bd5F70Fc83"
rewards = interface.IStakingRewards(rewardsAddress)

def stakeDQuick():
    dQuickAmount = dQuick.balanceOf(account, {"from": account})
    rewards.stake(dQuickAmount, {"from": account})

def main():
    stakeDQuick()