Feature: Edit Pipeline

    Scenario: I remove a source and add a source
        Given I am on the edit pipeline page
        And I have selected a source to add
        And I have selected a source to remove
        Then when I click Update the I should be redirected to the dashboard
        And the source added should be added and the source removed should be removed
