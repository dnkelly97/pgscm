Feature: Frontend template that other pages inherit from
    As a developer
    So that I have something to build upon
    I want to create a template within which the application is to be implemented

    Scenario: I can see the navigation bar
        Given I am on a page that inherits from the frontend template
        Then I should see a navigation bar

    Scenario Outline: I click <page> on the navigation bar
        Given I am on a page that inherits from the frontend template
        And I click the <page> option from the navigation bar
        Then I should be redirected to the <page> page

        Examples:
        | page |
        |Dashboard|
        |Student Portal|
        |Logout|
