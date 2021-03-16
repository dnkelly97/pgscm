Feature: Remove students from the system
  As an administrator
  So that I can keep the system up to date
  I want to be able to remove students from the system

  Scenario: Deleting student already in system
    Given I am logged in and on the student page
    When I create a student that I plan on removing
    When I click the delete button to remove this student
    Then I should be redirected to the delete student page
    Then I should see student removed on student portal
