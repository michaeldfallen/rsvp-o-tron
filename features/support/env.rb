# Urls for accessing RSVPOTRON
class Rsvpotron
  def self.url
    ENV['RSVPOTRON_URL'] || 'http://test:test@localhost:5000'
  end
end
