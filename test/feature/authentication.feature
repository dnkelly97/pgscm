Feature:
  As a developer
  So that I can control what different users can do
  I want to differentiate between an admin who can add users and an administrator who can simply just use the application

  Scenario: Access Create User Page as Admin
    Given I am an Admin
    When I want to access the 'register' page
    Then I get redirected to 'register' page

  Scenario: Access Create User Page as Administrator
    Given I am an Administrator
    When I want to access the 'register' page
    Then I get redirected back to 'dashboard' page

