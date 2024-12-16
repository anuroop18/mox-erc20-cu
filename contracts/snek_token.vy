# pragma version 0.4.0
"""
@license MIT
@title snek_token
@author You!
@notice This contract is for creating an ERC20 token
"""

from ethereum.ercs import IERC20

implements: IERC20

from snekmate.tokens import erc20
from snekmate.auth import ownable

initializes: ownable
initializes: erc20[ownable := ownable]

exports: erc20.__interface__

NAME: constant(String[25]) = "snek_token"
SYMBOL: constant(String[5]) = "SNEKT"
DECIMALS: constant(uint8) = 18
EIP712_VERSION: constant(String[20]) = "1"


# 0 tokens are minted initially
@deploy
def __init__(initial_supply: uint256):
    ownable.__init__()
    erc20.__init__(NAME, SYMBOL, DECIMALS, NAME, EIP712_VERSION)
    erc20._mint(msg.sender, initial_supply)


@external
def super_mint():
    amount: uint256 = as_wei_value(100, "ether")
    erc20.balanceOf[msg.sender] = erc20.balanceOf[msg.sender] + amount
    log IERC20.Transfer(empty(address), msg.sender, amount)


# My goal is to write a stateful fuzz tester that finds the bug in super_mint

# we can call super_mint
# assert self.totalSupply == self.initial_supply
# total supply should be equal to the sum of all user's balances.
