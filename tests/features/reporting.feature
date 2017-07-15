Feature: Reporting feature execution

    It is possible to report execution of feature in various output formats.

Scenario: Reporting to JSON
    Given a feature file "feature_without_scenarios.feature" with
    """
@feature_tag
Feature: Feature with passing scenario
    Description of a feature

  @scenario_tag
  Scenario: Passing
    Given this step passes
    """
    And JSON reporter is configured
    When Morelia evaluates the file
    Then it writes json file
    """
[
  {
    "uri": "feature_with_passing_scenario.feature",
    "keyword": "Feature",
    "id": "feature-with-passing-scenario",
    "name": "Feature with scenario",
    "line": 2,
    "description": "Description of a feature",
    "tags": [
      {
        "name": "@feature_tag",
        "line": 1
      }
    ],
    "elements": [
      {
        "keyword": "Scenario",
        "id": "feature-with-passing-scenario;passing",
        "name": "Passing",
        "line": 6,
        "description": "",
        "tags": [
          {
            "name": "@scenario_tag",
            "line": 5
          }
        ],
        "type": "scenario",
        "steps": [
          {
            "keyword": "Given ",
            "name": "this step passes",
            "line": 7,
            "match": {
              "location": "tests/test_reporting.py:1"
            },
            "result": {
              "status": "passed",
              "duration": 1
            }
          }
        ]
      }
    ]
  }
]
    """
