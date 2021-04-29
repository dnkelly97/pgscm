Feature: Activate Pipeline
  As an administrator
  So that I can activate or deactivate unwanted pipelines
  I want to be able to change their activity

  Scenario: Activate a pipeline (button)
        Given I am on the dashboard page
        When I have selected a pipeline
        Then a button should appear asking if I would like to activate pipeline

  Scenario: Activate a pipeline (popup)
        Given I am on the dashboard page
        And I have selected a pipeline
        When I click a button to activate the pipeline
        Then a modal will appear to confirm the activation

  Scenario: Activate a pipeline (confirm)
        Given I am on the dashboard page
        And I have selected a pipeline
        When I click a button to activate the pipeline
        And I confirm I want to activate the pipeline
        Then I should not see the pipeline on the menu
