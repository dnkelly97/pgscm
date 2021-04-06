Feature: Administrator Create Pipeline Form
    As an administrator
    So that I can manually create a pipeline
    I want to be able to fill out a form to create a pipeline

    Scenario: Change the number of stages
        Given I am on the create pipeline page
        When I change the number of stages
        Then I should see fields for creating a stage equal to the number of stages selected

    Scenario: I am on the create pipeline page and I successfully create a pipeline
        Given I am on the create pipeline page
        When I fill out a name: <name>
        When I fill out number of stages: <num_stages>
        And I click the create pipeline submit button
        Then I should be on the dashboard

    Scenario: I try to create a pipeline with a name that exists
        Given I am on the create pipeline page
        When I fill out a pipeline name that exists
        When I click the create pipeline submit button
        Then I should see an alert saying a pipeline with that name already exists
