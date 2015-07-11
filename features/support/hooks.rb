Before do
  visit("#{Rsvpotron.url}/invite")
  first(:button, 'Delete Invite').click while page.has_button?('Delete Invite')
end
