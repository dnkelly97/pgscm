Feature: Edit a saved query

    Scenario: Click edit query from dashboard
        Given I select a query from the dashboard page
        When I click the Edit Query button
        Then I should be redirected to the edit query page for the selected query

    Scenario: Change name field to valid name
        Given I am on the edit query page
        And I change the name of a query to an available name
        When I click the Update button
        Then I should be redirected to the dashboard page
        And the name of the query should be updated

    Scenario: Change name field to invalid name
        Given I am on the edit query page
        And I change the name of a query to an unavailable name
        When I click the Update button
        Then I should see a message telling me the query couldn't be saved
        And the name of the query should not be updated
