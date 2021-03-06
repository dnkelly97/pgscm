Feature: Delete Pipeline
    As an administrator
    So that I can remove unwanted pipelines
    I want to be able to delete pipelines

    Scenario: Delete a pipeline (dashboard)
        Given I am on the dashboard page
        And I have selected a pipeline
        When I click the dashboard Delete Pipeline button
        Then a popup should appear asking me to confirm

    Scenario: Delete a pipeline (popup)
        Given I am on the dashboard page and the confirm delete pipeline popup is visible
        When I click the popup Delete button
        Then I should see a confirmation message
        And I should not see the pipeline I selected listed anymore

    Scenario: Delete multiple pipelines
        Given I am on the dashboard page and the confirm delete pipeline popup is visible
        When I click the popup Delete button
        And I go to delete another pipeline from the dashboard
        And I click the popup Delete button again
        Then neither of the pipelines I deleted should be listed anymore
