Feature: Administrator Create Student Form
    As an administrator
    So that I can manually create a student
    I want to be able to fill out a form to create a student

    Scenario: I am on the create student page and I successfully create a student
        Given I am on the create student page
        When I fill out a email: <email>
        And I fill out a first name: <first_name>
        And I fill out a last name: <last_name>
        And I click the create student submit button
        Then I should be on the student portal