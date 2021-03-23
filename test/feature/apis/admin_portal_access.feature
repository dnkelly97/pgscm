Feature:
  As a developer
  So that I can control what different users can do
  I want to differentiate between an admin who can add apis and an administrator who can simply just use the application

  Scenario: Access Admin Portal as Admin
    Given I am an Admin
    When I want to access the 'api portal' page
    Then I get redirected to 'api portal' page

  Scenario: Access Admin Portal as Administrator
    Given I am an Administrator
    When I want to access the 'api portal' page
    Then I get redirected back to 'dashboard' page