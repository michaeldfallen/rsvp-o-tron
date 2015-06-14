require 'pry'

Given(/^I completed my RSVP$/) do
  step 'I have responded that I will attend with bells on!'
  step 'I choose turkey for my menu choice'
end

Given(/^I have already responded$/) do
  step 'I am invited to the wedding'
  step 'I completed my RSVP'
end

When(/^I enter my RSVP code$/) do
  visit("#{$URL}/rsvp")
  fill_in('token', :with => "#{@invite_id}")
  click_button('Continue')
end

When(/^I am taken straight to the confirmation page$/) do
  assert(current_url.end_with?("rsvp/#{@invite_id}"))
end

When(/^I am taken to the confirmation page$/) do
  assert(current_url.end_with?("rsvp/#{@invite_id}/finished"))
end

Then(/^my answers are displayed$/) do
  assert(page.has_content?("John is having the Turkey and Ham"))
end
