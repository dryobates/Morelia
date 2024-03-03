@feature_label
Feature: Labels support

    Labels are texts appended to feature, scenario or step and starts with @ sign.
    They can be accessed inside your test steps and setUp hooks as additional information.

    @scenario_label
    Scenario: Scenario with labels
        When step which accepts _labels variable is executed
        Then it will get labels "feature_label,scenario_label"

    @label1 @label2
    Scenario: Scenario with multiply labels
        When step which accepts _labels variable is executed
        Then it will get labels "feature_label,label1,label2"

    @scenario_label
    Scenario: Scenario with steps that do not accept _labels
        When step which does not accepts _labels variable is executed
        Then it will not get any labels

    @scenario_label
    Scenario: Step with labels
        @when_label
        When step which accepts _labels variable is executed
        Then it will get labels "feature_label,scenario_label,when_label"

    @scenario_label
    Scenario: setUpFeature gets labels
        When setUpFeature hook is called
        Then it will get labels "feature_label"

    @scenario_label
    Scenario: setUpScenario gets labels
        When setUpScenario hook is called
        Then it will get labels "feature_label,scenario_label"

    @scenario_label
    Scenario: setUpStep gets labels
        @step_label
        When setUpStep hook is called
        Then it will get labels "feature_label,scenario_label,step_label"
