Feature:
  As an Admin
  So that I can view all of the information for a particular API Key
  I want to select an API Key in the Admin Portal and view its detailed information on another page

  Scenario: Access API profile as an Admin
    Given I am an Admin
    When I want to access the 'api profile' page
    Then I get redirected to 'api profile' page