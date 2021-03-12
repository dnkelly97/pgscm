Feature: Student Querying Interface
  As an administrator
  So that I can find student matching certain criteria
  I want to be able to search for students based on available criteria

  Scenario: List students currently in the system
    Given I know some users are already in the system
    When I go to the 'dashboard'
    Then I should see the students currently in the system

  Scenario: Query students based on specific attributes
    Given I know some users are already in the system
    And I have some attributes to sort students by
    When I go to the queried 'dashboard'
    Then I should be able to filter students based on those attributes