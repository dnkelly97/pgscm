Feature: Update student info within application
  As an administrator
  So that I can update information about a student that has already been added to the system
  I want to be able to edit student information manually within the application

  Scenario: Update student information
    Given I am logged in and on the student page
    When I create a student that I plan on updating
    When I click the update button to update this student's information
    Then I should be redirected to the update student page
    Then I should see the updated student on the student portal