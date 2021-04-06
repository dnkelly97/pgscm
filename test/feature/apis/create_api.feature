Feature:
  As a developer
  So that I can control what different users can do
  I want to differentiate between an admin who can add apis and an administrator who can simply just use the application

  Scenario Outline: Submit New API Key
    Given I am an Admin
    And I access the Create API Form
    When I fill out the Create API Form with <name>, <email>, <expiration_date>
    Then the API key was <saved>

    Examples:
      | name   | email            | expiration_date | saved     |
      | Tester | Tester@gmail.com | 06/20/2020      | saved     |
      | Tester | Tester@gmail.com |                 | saved     |
      |        | Tester@gmail.com | 06/20/2020      | not saved |
      | Tester | Tester           |                 | not saved |

