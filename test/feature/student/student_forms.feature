Feature One Time Research Interest Form
  As an administrator
  So that I can collect student information from students and have the information be identifiable and have each form only be filled out once
  I want to be able to generate form links that are usable only once and linked to a student

  Scenario: Email can be sent to student to create full profile
    Given I am an administrator
    When I go to the Student Portal and click Request Information Button
    Then I should be prompted to enter a student's email

  Scenario: Email a student with a particular email
    Given I am an administrator
    When I go to the Student Portal and click Request Information Button
    When I enter an email to send the form to
    Then I should get a confirmation message saying I so successfully

  Scenario: Enter an invalid email
    Given I am an administrator
    When I go to the Student Portal and click Request Information Button
    When I enter an invalid email format
    Then I should get an error message saying that something went wrong