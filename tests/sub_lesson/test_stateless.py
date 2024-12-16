import pytest
from boa.test.strategies import strategy
from hypothesis import HealthCheck, given, settings

from contracts.sub_lesson import stateless_fuzz_solvable


@pytest.fixture(scope="function")
def contract():
    return stateless_fuzz_solvable.deploy()

@settings(max_examples=10000, 
          suppress_health_check=[HealthCheck.function_scoped_fixture]
          )
@given(input=strategy("uint256"))
def test_always_returns_input(contract, input):
    print(input)
    assert contract.always_returns_input_number(input) == input