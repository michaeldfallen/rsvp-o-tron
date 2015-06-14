Feature: Rooms
  As a guest who has a room held for me
  I want to be told how to book it
  so that I don't miss out on my room

Acceptance Criteria
- A message is placed on the confirmation screen if you have a room held

  Scenario: I don't have a room held
    Given I have already responded
    When I am taken to the confirmation page
    Then no room message is displayed

  Scenario: I have a room held
    Given I have a room held for me on my invite
    When I completed my RSVP
    And I am taken to the confirmation page
    Then a message telling me I have a room is displayed
