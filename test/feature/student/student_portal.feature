Feature: Administrator View Student Portal
    As an administrator
    So that I interact with students in the database
    I want to have the needed components

    Scenario: I am on the student page and I want to create a student
        Given I am on the student portal
        And I should see a button for creating a new student
        When I click the create student button
        Then I should see a create student form
        Then I should see a create student button

   Scenario: I send an email to particular student
       Given I am on the student portal
       When I click on the Request Information Button
       When I enter the student's email
       Then I should see a response message
