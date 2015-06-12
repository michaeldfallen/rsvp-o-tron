Feature: Confirmation page
  As a guest who has already responded
  I want to view my responses
  so that I don't forget if I ordered turkey or beef

Acceptance criteria
- If you enter the RSVP code again after responding you're taken straight to the confirmation page
- You're answers are replayed to you on the confirmation page

Scenario: Checking my answers
    Given I have already responded
    When I enter my RSVP code
    Then I am taken to the confirmation page
    And my answers are displayed

Scenario: Finishing my response
    Given I am invited to the wedding
    And I completed my RSVP
    When I am taken to the confirmation page
    Then my answers are displayed
