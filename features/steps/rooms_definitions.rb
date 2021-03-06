require 'pry'

Then(/^no room message is displayed$/) do
  assert(page.has_content?("We'll see you there"))
  assert(page.has_content?('A room has been held for you') == false)
end

Then(/^a message telling me I have a room is displayed$/) do
  assert(page.has_content?("We'll see you there"))
  assert(page.has_content?('A room has been held for you'))
end

Given(/^I have a room held for me on my invite$/) do
  visit("#{Rsvpotron.url}/invite")
  click_on('Create new invite')
  find('label', text: 'Room held').trigger('click')
  click_button('Continue')
  click_button('Add Guest')
  fill_in('First Name', with: 'John')
  fill_in('Last Name', with: 'Smith')
  click_button('Continue')
  @invite_id = find('.token').text
end
