Feature One Time Demographics Form
  As an prospective graduate student
  So that I can be applied in emails relating to my demographic information
  be able to fill out a form containing that information

  Scenario: Send out Demographics Form to Prospective Student
    Given I am an Administrator
    When I access the Student Portal
    And I create a specific user
    And I access that user's profile page
    And I press the 'Request Update' button
    Then I should get a response that the email was sent successfully
    Then I should be able to enter the Form url for that user

  Scenario: Access Demographics Form
    Given I am an Administrator
    When I access the Student Portal
    And I create a specific user
    And I access that user's profile page
    And I press the 'Request Update' button
    And I go to Demographics Form Page
    And I submit the form as is
    Then I should get a confirmation message
    Then I should no longer be able to access this page