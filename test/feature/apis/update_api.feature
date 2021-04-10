Feature:
  As a developer
  So that I can control what different users can do
  I want to differentiate between an admin who can add apis and an administrator who can simply just use the application

  Scenario Outline: Update API Key Page Redirect
    Given I am an Admin
    And I go to the api portal
    And I select an API Form with <name>, <email>, <expiration_date> to view
    When I select the update API Key button
    Then I should see 'Update <name>' on the Update Page

    Examples:
      | name   | email            | expiration_date |
      | Tester | Tester@gmail.com | 06/20/2020      |

  Scenario Outline: Update API Key Page Submit
    Given I am an Admin
    And I go to the api portal
    And I select an API Form with <name>, <email>, <expiration_date> to view
    When I select the update API Key button
    And I fill out the update form with a <new_name>, <new_email>, <new_expiration_date>
    Then I should see <new_name>, <new_email>, <new_expiration_date> on the API Key's profile page

    Examples:
      | name   | email            | expiration_date | new_name  | new_email            | new_expiration_date |
      | Tester | Tester@gmail.com | 06/20/2020      | NewTester | NewTester@gmail.com  | 06/20/2022          |