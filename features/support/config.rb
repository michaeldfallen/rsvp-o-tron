require 'capybara/cucumber'
require 'capybara/poltergeist'

include Capybara::DSL
Capybara.default_wait_time = 5
Capybara.app_host = 'http://localhost:5000'

Capybara.default_driver = :poltergeist
Capybara.javascript_driver = :poltergeist

Capybara.register_driver :poltergeist do |app|
  Capybara::Poltergeist::Driver.new(app, inspector: true, js_errors: true)
end

### Configure Assertions so we can add assertions like assert_match() in tests
require 'test/unit'
include Test::Unit::Assertions
