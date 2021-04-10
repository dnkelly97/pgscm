Feature:
  As a developer
  So that I can control what different users can do
  I want to differentiate between an admin who can add apis and an administrator who can simply just use the application

  Scenario Outline: Regenerate API Key Popup Confirmation
    Given I am an Admin
    And I go to the api portal
    And I select an API Form with <name>, <email>, <expiration_date> to view
    When I select the regenerate API Key button
    Then I should see a popup modal appear to confirm the regeneration of the key

    Examples:
      | name   | email            | expiration_date |
      | Tester | Tester@gmail.com | 06/20/2020      |

  Scenario Outline: Regenerate API Key Cancel Modal
    Given I am an Admin
    And I go to the api portal
    And I select an API Form with <name>, <email>, <expiration_date> to view
    When I select the regenerate API Key button
    And I cancel my regenerate API Key command
    Then I should see <name>, <email> or <expiration_date> on the api profile page

    Examples:
      | name   | email            | expiration_date |
      | Tester | Tester@gmail.com | 06/20/2020      |

  Scenario Outline: Regenerate API Key
    Given I am an Admin
    And I go to the api portal
    And I select an API Form with <name>, <email>, <expiration_date> to view
    When I select the regenerate API Key button
    And I confirm I want to regenerate the API Key
    Then I should see <name>, <email> or <expiration_date> on the api profile with a new prefix

    Examples:
      | name   | email            | expiration_date |
      | Tester | Tester@gmail.com | 06/20/2020      |