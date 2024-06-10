require_relative "boot"

require "rails/all"
require 'devise'
require 'dotenv/rails-now'
# Require the gems listed in Gemfile, including any gems
# you've limited to :test, :development, or :production.
Bundler.require(*Rails.groups)

module FasthuntWebsite
  class Application < Rails::Application
    # Initialize configuration defaults for originally generated Rails version.
    config.load_defaults 7.1

    # Please, add to the `ignore` list any other `lib` subdirectories that do
    # not contain `.rb` files, or that should not be reloaded or eager loaded.
    # Common ones are `templates`, `generators`, or `middleware`, for example.
    config.autoload_lib(ignore: %w(assets tasks))

    config.middleware.use OmniAuth::Builder do
      provider :google_oauth2, '871004138248-tds28o3351kg28l55ksmvpncajfobk3p.apps.googleusercontent.com', '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', {
        scope: 'email,profile',
        prompt: 'select_account'
      }
    end
    # Configuration for the application, engines, and railties goes here.
    #
    # These settings can be overridden in specific environments using the files
    # in config/environments, which are processed later.
    #
    # config.time_zone = "Central Time (US & Canada)"
    # config.eager_load_paths << Rails.root.join("extras")
  end
end
