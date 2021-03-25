Feature: Run a saved query

    Scenario: Run a saved query
        Given I select a query from the dashboard
        When I click the Run Query button
        Then I should see students that met the query conditions displayed on the student page
        And I should not see other students