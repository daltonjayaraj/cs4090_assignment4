
Feature: Add task

  Scenario: User adds a new task
    Given an empty task list
    When the user adds a task titled "Buy bread"
    Then there should be 1 task in the list
