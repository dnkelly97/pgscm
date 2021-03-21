Feature: Save a query

    As an administrator
    So that I can reuse queries later, such as to source pipelines
    I want to be able to save queries I write

    Background:
        Given there is a saved query in the database with name 'Query 0'

    Scenario: Open save query popup
        Given I am on the student page
        And I click the save query button
        Then a popup should appear
        And the popup should have fields for entering query name and query description

    Scenario Outline: Click 'Save Query' button on the popup
        Given I fill out the query name with <name>
        When I click the 'Save Query' button
        Then I should see an alert in the popup saying <message>
        And the alert should be <color>

        Examples:
        |name|message|color|
        | my query | Query successfully saved! | green |
        | my queryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy   |   Save Failed - Query names must be less than 60 characters in length.    |  red  |
        |    | Save Failed - Invalid query name.   | red |
        | Query 0 | Save Failed - A query with this name already exists. | red |
