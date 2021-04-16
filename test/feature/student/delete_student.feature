Feature: Remove students from the system
  As an administrator
  So that I can keep the system up to date
  I want to be able to remove students from the system

  Scenario Outline: Delete Student Popup Confirmation
    Given I am logged in and on the student page
    And I create a student that I plan on removing
    When I click the delete button to remove this student
    Then I should see a modal popup to confirm I want to delete a student

  Scenario Outline: Delete Student Popup Cancel
    Given I am logged in and on the student page
    And I create a student that I plan on removing
    When I click the delete button to remove this student
    And I cancel the deletion of the student
    Then I should still be on the student's profile page

  Scenario Outline: Delete Student Submit
    Given I am logged in and on the student page
    And I create a student that I plan on removing
    When I click the delete button to remove this student
    And I confirm I want to remove this student
    Then I should not see the student on the student portal page
