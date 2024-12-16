from boa.test.strategies import strategy
from hypothesis import settings
from hypothesis.stateful import RuleBasedStateMachine, rule

from contracts.sub_lesson import stateful_fuzz_solvable


class StatefulFuzzer(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.contract = stateful_fuzz_solvable.deploy()
        print("Deployed contract")
    
    # "Rule" -> Actions, can have properties/invariants
    # "Invariants" -> Properties that should always hold true
    @rule(new_number=strategy("uint256"))
    def change_number(self, new_number):
        self.contract.change_number(new_number)
        print(f"    Called change_number with {new_number}")

    @rule(input=strategy("uint256"))
    def input_number_returns_itself(self, input):
        response = self.contract.always_returns_input_number(input)
        print(f"    Called input_number_returns_itself with {input}")
        assert response == input, f"Expected {input}, got {response}"

TestStatefulFuzzing = StatefulFuzzer.TestCase
TestStatefulFuzzing.settings = settings(max_examples=100, stateful_step_count=50)