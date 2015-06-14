require 'pry'

Then(/^no room message is displayed$/) do
  assert(page.has_content?('Thank you for your response'))
  assert(page.has_content?('A room has been held for you') == false)
end

Then(/^a message telling me I have a room is displayed$/) do
  assert(page.has_content?('Thank you for your response'))
  assert(page.has_content?('A room has been held for you'))
end

Given(/^I have a room held for me on my invite$/) do
  visit("#{$URL}/invite")
  click_on('Create new invite')
  check('Room held')
  click_button('Continue')
  click_button('Add Guest')
  fill_in('First Name', :with => 'John')
  fill_in('Last Name', :with => 'Smith')
  click_button('Continue')
  @invite_id = find('.token').text
end
