from pytest_bdd import scenario, given, when, then


@scenario('../feature/creating_roles.feature', 'Access Create User Page as Admin')
def test_user_roles_admin():
    pass


@given("I am an Admin")
def admin_access(admin_user):
    pass


@when("I want to access the 'register' page")
def connect_register(admin_user):
    pass


@then("I get redirected to 'register' page")
def redirect_register():
    pass


@scenario('../feature/creating_roles.feature', 'Access Create User Page as Administrator')
def test_user_roles_administrator():
    pass


@given("I am an Administrator")
def administrator_access(admin_client):
    pass


@then("I get redirected back to 'dashboard' page")
def redirect_dashboard():
    pass
