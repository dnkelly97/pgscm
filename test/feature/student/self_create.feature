Feature One Time Research Interest Form
  As a student
  So that I can submit my information as a potential graduate student
  I want to be able to fill in a form that has this information

  Scenario: Check accessibility to form online
    Given I am a student
    When I click the link to access the form
    Then I should be able to enter my information

  Scenario: Confirm student are being created with this student form
    Given I am an Administrator
    When a student creates a profile
    And I go to the Student Portal
    Then I should see the student in the database

  Scenario: Check fail and success student creation
    Given I am a student
    When I click the link to access the form
    When I press the submit button without information
    Then I should see an error message
    When I press the submit button with information
    Then I should see a success message
