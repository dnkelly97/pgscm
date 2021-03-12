Feature:
  As an administrator
  So that I securely enter into the program
  I want to be able to login into the application

  Scenario: Login into the application as an Administrator
    Given I am an Administrator
    When I want to login into the application with correct information
    Then I get access to 'dashboard'

  Scenario: Login into the application with wrong credentials
    Given I am an Administrator
    When I want to login into the application with incorrect information
    Then I stay on the login page

