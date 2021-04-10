Feature:
  As a developer
  So that I can control what different users can do
  I want to differentiate between an admin who can add apis and an administrator who can simply just use the application

  Scenario Outline: Delete API Key Popup Confirmation
    Given I am an Admin
    And I go to the api portal
    And I select an API Form with <name>, <email>, <expiration_date> to view
    When I select the delete API Key button
    Then I should see a popup modal appear to confirm the deletion of the key

    Examples:
      | name   | email            | expiration_date |
      | Tester | Tester@gmail.com | 06/20/2020      |

  Scenario Outline: Delete API Key Cancel Modal
    Given I am an Admin
    And I go to the api portal
    And I select an API Form with <name>, <email>, <expiration_date> to view
    When I select the delete API Key button
    And I cancel my delete API Key command
    Then I should see <name>, <email> or <expiration_date> on the api profile page

    Examples:
      | name   | email            | expiration_date |
      | Tester | Tester@gmail.com | 06/20/2020      |

  Scenario Outline: Delete API Key
    Given I am an Admin
    And I go to the api portal
    And I select an API Form with <name>, <email>, <expiration_date> to view
    When I select the delete API Key button
    And I confirm I want to delete the API Key
    Then I should not see <name>, <email> or <expiration_date> on the api portal

    Examples:
      | name   | email            | expiration_date |
      | Tester | Tester@gmail.com | 06/20/2020      |



