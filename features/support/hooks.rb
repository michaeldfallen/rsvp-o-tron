Before do
  visit("#{$URL}/invite")
  while page.has_button?('Delete Invite') do
    click_button('Delete Invite')
  end
end
