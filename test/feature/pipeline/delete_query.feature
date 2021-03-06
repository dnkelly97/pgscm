Feature: Delete Query
    As an administrator
    So that I can remove unwanted queries
    I want to be able to delete queries

    Scenario: Delete a query (dashboard)
        Given I am on the dashboard page
        And I have selected a query
        When I click the dashboard Delete Query button
        Then a popup should appear asking me to confirm

    Scenario: Delete a query (popup)
        Given I am on the dashboard page and the confirm delete query popup is visible
        When I click the popup Delete button
        Then I should see a confirmation message
        And I should not see the query I selected listed anymore

    Scenario: Delete multiple queries
        Given I am on the dashboard page and the confirm delete query popup is visible
        When I click the popup Delete button
        And I go to delete another query from the dashboard
        And I click the popup Delete button again
        Then neither of the queries I deleted should be listed anymore