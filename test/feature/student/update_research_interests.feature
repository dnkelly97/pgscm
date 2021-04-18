Feature One Time Research Interest Form
  As an administrator
  So that I can collect student information from students and have the information be identifiable and have each form only be filled out once
  I want to be able to generate form links that are usable only once and linked to a student

  Scenario: Send out Research Interest Form to Prospective Student
    Given I am an Administrator
    When I access the Student Portal
    And I create a specific user
    And I access that user's profile page
    And I press the 'Request Update' button
    Then I should get a response that the email was sent successfully
    Then I should be able to enter the Form url for that user

  Scenario: Access Research Interests Form
    Given I am an Administrator
    When I access the Student Portal
    And I create a specific user
    And I access that user's profile page
    And I press the 'Request Update' button
    And I go to Research Interests Form Page
    And I submit the form as is
    Then I should get a confirmation message
    Then I should no longer be able to access this page