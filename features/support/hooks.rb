Before do
  visit("#{$URL}/invite")
  while page.has_button?('Delete Invite') do
    first(:button, 'Delete Invite').click
  end
end
