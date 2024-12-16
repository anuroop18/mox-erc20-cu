import boa
import pytest

from script.deploy import INITIAL_SUPPLY, deploy

RANDOM_USER = boa.env.generate_address("random_user")


def test_token_supply():
    snek_token = deploy()

    assert snek_token.totalSupply() == INITIAL_SUPPLY
    assert snek_token.balanceOf(snek_token.owner()) == INITIAL_SUPPLY


def test_token_emits_event():
    snek_token = deploy()
    with boa.env.prank(snek_token.owner()):
        snek_token.transfer(RANDOM_USER, INITIAL_SUPPLY)
        logs = snek_token.get_logs()
        log_owner = logs[0].topics[0]
        assert log_owner == snek_token.owner()
    assert snek_token.balanceOf(RANDOM_USER) == INITIAL_SUPPLY
    assert snek_token.balanceOf(snek_token.owner()) == 0

def test_transfer():
    snek_token = deploy()
    transfer_amount = INITIAL_SUPPLY // 2

    with boa.env.prank(snek_token.owner()):
        snek_token.transfer(RANDOM_USER, transfer_amount)

    assert snek_token.balanceOf(RANDOM_USER) == transfer_amount
    assert snek_token.balanceOf(snek_token.owner()) == INITIAL_SUPPLY - transfer_amount

def test_transfer_insufficient_balance():
    """Test transfer fails when sender lacks sufficient balance"""
    snek_token = deploy()
    
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("erc20: transfer amount exceeds balance"):
            snek_token.transfer(snek_token.owner(), INITIAL_SUPPLY)