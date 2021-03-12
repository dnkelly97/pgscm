Feature: Frontend template that other pages inherit from
    As a developer
    So that I have something to build upon
    I want to create a template within which the application is to be implemented

    Scenario: I can see the navigation bar
        Given I am on a page that inherits from the frontend template
        Then I should see a navigation bar

    Scenario: I click 'Dashboard' on the navigation bar
        Given I am on a page that inherits from the frontend template
        And I click the 'Dashboard' option from the navigation bar
        Then I should be redirected to the dashboard page

    Scenario: I click 'Students' on the navigation bar
        Given I am on a page that inherits from the frontend template
        And I click the 'Dashboard' option from the navigation bar
        Then I should be redirected to the dashboard page
