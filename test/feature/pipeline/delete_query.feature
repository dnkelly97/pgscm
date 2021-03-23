Feature: Delete Query
    As an administrator
    So that I can remove unwanted queries
    I want to be able to delete queries

    Scenario: Delete a query
        Given I am on the dashboard page
        And I have selected a query
        When I click the Delete Query button
        Then I should not see the query listed anymore