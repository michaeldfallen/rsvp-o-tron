Feature: Child guests
  As the lucky couple
  I want to identify some guests as children
  so that I know who to give half portions to

Acceptance criteria
- When answering the menu choice question children are offered a half portion of the full adult main course

Scenario: Inviting a child
    Given I have created an invite
    When I add a child guest to that invite
    Then they are listed on the invite list as a child

Scenario: Children offered half portion
    Given I am a child invited to the wedding
    When I am on the menu choice page
    Then I am offered a half portion
