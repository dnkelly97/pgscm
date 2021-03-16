Feature: Administrator Create Pipeline Form
    As an administrator
    So that I can manually create a pipeline
    I want to be able to fill out a form to create a pipeline

    Scenario: I am on the create pipeline page and I successfully create a pipeline
        Given I am on the create pipeline page
        When I fill out a name: <name>
        And I click the create pipeline submit button
        Then I should be on the dashboard