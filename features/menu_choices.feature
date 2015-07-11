Feature: Guests dinner choices
  In order to have an idea of what to cook
  the Caterer needs Guests
  to choose their main course when RSVPing

Acceptance criteria
- Beef, Turkey and Veg are all okay options
- Guest shouldn't be asked for a main course if not attending


Scenario: Guest wants beef
    Given I am invited to the wedding
    When I have responded that I will attend with bells on!
    And I choose beef for my menu choice
    Then my RSVP has the menu choice beef

Scenario: Guest wants turkey
    Given I am invited to the wedding
    When I have responded that I will attend, free of bells
    And I choose turkey for my menu choice
    Then my RSVP has the menu choice turkey

Scenario: Guest wants vegetarian
    Given I am invited to the wedding
    When I have responded that I will attend, undecided on bells
    And I choose tarte tatin for my menu choice
    Then my RSVP has the menu choice vegetarian

Scenario: Guest not attending
    Given I am invited to the wedding
    When I have responded that I will not attend... I heard there would be people with bells
    Then I am not asked for a menu choice
    And my RSVP has no recorded menu choice

Scenario: Guest not attending
    Given I am invited to the wedding
    When I have responded that I will not attend... I heard there would be people with bells
    Then I am not asked for a menu choice
    And my RSVP has no recorded menu choice
