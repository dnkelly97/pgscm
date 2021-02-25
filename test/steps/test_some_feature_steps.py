from pytest_bdd import scenario, given, then, when


# the scenario marked method runs like a normal pytest test, after all associated steps have been run
# it must start with test_
@scenario("../feature/some_feature.feature", "Some imaginary scenario")
def test_some_feature_scenario():
    pass


# example of one step aliased with two different given/when statements
@given("I do some action")
@given("Some setup condition")
def fake_step():
    print("fake step")


@then("Some other condition should be achieved")
def fake_assertion_step():
    print("fake assertion step")
    assert 1 == 1
