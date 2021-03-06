Feature:
  As an admin
  So that I can enable administrators to use the application
  I want to be able to create accounts for them

  Scenario: Create New User as an Admin
    Given I am an Admin
    When I want to create a new user
    Then I get redirected back to 'dashboard' page

  Scenario: Unable to create user as non admin
    Given I am a non admin user
    When I login into the application
    Then I cannot use a register button
