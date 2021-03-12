from pytest_bdd import scenario, given, when, then
import pytest
from django.contrib.auth.models import User
from student.models import Student
from selenium.webdriver.common.keys import Keys


@pytest.mark.django_db
@scenario("../../feature/student/student_querying.feature", "List students currently in the system")
def test_student_list(live_server):
    pass


@given("I know some users are already in the system")
def students_setup(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)


@when("I go to the 'dashboard'")
def dashboard_location(live_server, browser):
    student = Student.objects.create(email='hello@gmail.com', first_name='Joe', last_name='Chaplin')
    student.save()
    student2 = Student.objects.create(email='hello12@gmail.com', first_name='Joey', last_name='Morrow')
    student2.save()
    browser.get(live_server + '/student')


@then("I should see the students currently in the system")
def check_list(browser):
    assert browser.find_element_by_id('id_dashboard')
    assert "hello@gmail.com" in browser.page_source


@pytest.mark.django_db
@scenario("../../feature/student/student_querying.feature", "Query students based on specific attributes")
def test_student_query(live_server):
    pass


@given("I have some attributes to sort students by")
def setup_attributes(live_server, browser):
    browser.get(live_server + '/student')


@when("I go to the queried 'dashboard'")
def queried_dashboard(browser):
    browser.find_element_by_id('id_name').send_keys('Joe')
    browser.find_element_by_id('id_submit_filter').click()


@then("I should be able to filter students based on those attributes")
def check_filter_students(browser):
    assert "Joe" in browser.page_source
    assert "Joey" not in browser.page_source
