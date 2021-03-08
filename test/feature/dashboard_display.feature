Feature: Dashboard Displays Pipelines and Queries
    As an administrator
    So that I can see my created pipelines and saved queries
    I want to have a dashboard page displaying that information

    Scenario: I am on the dashboard page
        Given I am on the dashboard
        Then I should see existent pipelines
        Then I should see existent saved queries
        Then I should see buttons for creating, deleting, and editing pipelines
        Then I should see buttons for creating, deleting, and editing saved queries
        Then each pipeline and query should have a checkbox to select it
