# Be sure to restart your server when you modify this file.

# Version of your assets, change this if you want to expire all your assets.
Rails.application.config.assets.version = "1.0"

# Add additional assets to the asset load path.
# Rails.application.config.assets.paths << Emoji.images_path

# Precompile additional assets.
Rails.application.config.assets.precompile += %w( projects.js )
Rails.application.config.assets.precompile += %w( profile_checkmarks.js )
Rails.application.config.assets.precompile += %w( project_checkmarks.js )
Rails.application.config.assets.precompile += %w( combined_checkmarks.js )
Rails.application.config.assets.precompile += %w( dropdownFunctionality.js )
Rails.application.config.assets.precompile += %w( user_session_tracker.js )


Rails.application.config.assets.precompile += %w( rails-ujs.js )
# application.js, application.css, and all non-JS/CSS in the app/assets
# folder are already added.
# Rails.application.config.assets.precompile += %w( admin.js admin.css )
