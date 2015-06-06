require 'pry'

Given(/^I am invited to the wedding$/) do
  visit("#{$URL}/invite")
  click_on('Create new invite')
  click_button('Continue')
  click_button('Add Guest')
  fill_in('First Name', :with => 'John')
  fill_in('Last Name', :with => 'Smith')
  click_button('Continue')
  @invite_id = find('.token').text
end

When(/^I have responded that I will (gladly|resentfully) attend$/) do |feels|
  visit("#{$URL}/rsvp")
  fill_in('token', :with => "#{@invite_id}")
  click_button('Continue')
  page.has_content?("You are invited to our wedding")
  click_button('Continue')
  choose("I will #{feels} attend")
  click_button("Continue")
end

When(/^I have responded that I will not attend$/) do
  visit("#{$URL}/rsvp")
  fill_in('token', :with => "#{@invite_id}")
  click_button('Continue')
  page.has_content?("You are invited to our wedding")
  click_button('Continue')
  choose("I regretfully decline")
  click_button("Continue")
end

When(/^I choose (turkey|beef|vegetarian) for my menu choice$/) do |main|
  choose(main)
  click_button("Continue")
end

Then(/^I am not asked for a menu choice$/) do
  assert(current_url.end_with?('finished'))
end

Then(/^my RSVP has no recorded menu choice$/) do
  visit("#{$URL}/invite")
  assert(!page.has_content?("vegetarian"))
  assert(!page.has_content?("turkey"))
  assert(!page.has_content?("beef"))
end

Then(/^my RSVP has the menu choice (turkey|beef|vegetarian)$/) do |main|
  visit("#{$URL}/invite")
  assert(page.has_content?(main))
end


