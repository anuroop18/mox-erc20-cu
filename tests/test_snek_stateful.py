import boa
from boa.test.strategies import strategy
from eth.constants import UINT_256_MAX
from hypothesis import assume, settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, initialize, invariant, rule

from script.deploy import deploy

MINTERS_SIZE = 10


class TokenStatefulFuzzer(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()

    @initialize()
    def setup(self):
        self.contract = deploy()
        self.minters = [boa.env.generate_address() for _ in range(MINTERS_SIZE)]

    @rule(
        amount=strategy("uint256"),
        minter_seed=st.integers(min_value=0, max_value=MINTERS_SIZE - 1),
    )
    def mint(self, amount, minter_seed):
        assume(self.contract.totalSupply() + amount < UINT_256_MAX)
        address = self.minters[minter_seed]
        self.contract.mint(address, amount)

    @rule(
        minter_seed=st.integers(min_value=0, max_value=MINTERS_SIZE - 1),
    )
    def super_mint(self, minter_seed):
        address = self.minters[minter_seed]
        with boa.env.prank(address):
            self.contract.super_mint()

    @invariant()
    def user_balance_should_never_exceed_total_supply(self):
        total_supply = self.contract.totalSupply()
        for address in self.minters:
            balance = self.contract.balanceOf(address)
            assert (
                balance <= total_supply
            ), f"Address {address} balance exceeds total supply"


TestTokenStatefulFuzzing = TokenStatefulFuzzer.TestCase
TestTokenStatefulFuzzing.settings = settings(max_examples=1000, stateful_step_count=50)
