Feature: Select Form For Stage

    Scenario: I select a form to be sent with a stage when creating a pipeline
        Given I am on the create pipeline page
        And I have filled out a pipeline's required fields
        When I change the advancement condition of a stage to 'Form Received'
        Then I should see an option to select the demographics form or the research interests form

    Scenario: I create a pipeline with 'Form Received' advancement condition
        Given I create a pipeline with a stage that has 'Form Received' as the advancement condition
        Then that stage should have the correct form associated with it
