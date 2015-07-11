require 'pry'

Given(/^I have created an invite$/) do
  visit("#{Rsvpotron.url}/invite")
  click_on('Create new invite')
  click_button('Continue')
  @invite_id = find('.token').text
end

When(/^I add a child guest to that invite$/) do
  click_button('Add Guest')
  fill_in('First Name', with: 'John')
  fill_in('Last Name', with: 'Smith')
  check('Child')
  click_button('Continue')
end

Then(/^they are listed on the invite list as a child$/) do
  assert(page.has_content?('Child Guest'))
end

Given(/^I am a child invited to the wedding$/) do
  step('I have created an invite')
  step('I add a child guest to that invite')
end

When(/^I am on the menu choice page$/) do
  visit("#{Rsvpotron.url}/")
  fill_in('token', with: @invite_id)
  click_button('Continue')
  page.has_content?('You are invited to our wedding')
  click_button('Continue')
  find('label', text: 'I will be there with bells on!').trigger('click')
  click_button('Continue')
  assert(current_url.end_with?('menu-choice'))
end

Then(/^I am offered a half portion$/) do
  assert(page.has_content?('A half portion of', count: 3))
end
