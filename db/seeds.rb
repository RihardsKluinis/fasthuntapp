# This file should ensure the existence of records required to run the application in every environment (production,
# development, test). The code here should be idempotent so that it can be executed at any point in every environment.
# The data can then be loaded with the bin/rails db:seed command (or created alongside the database with db:setup).
#
# Example:
#
#   ["Action", "Comedy", "Drama", "Horror"].each do |genre_name|
#     MovieGenre.find_or_create_by!(name: genre_name)
#   end
require 'json'

# Read JSON data from projects.json file
file = File.read(Rails.root.join('db', 'data', 'projects.json'))
json_data = JSON.parse(file)

# Use ActiveRecord transaction to ensure atomicity of database operations
ActiveRecord::Base.transaction do
  # Iterate over each project in the JSON data
  json_data['projects'].each do |key, project_attributes|
    # Access attributes of the project
    project_id_value = project_attributes['project_id']
    website = project_attributes['website']
    name = project_attributes['title']
    date = project_attributes['date']
    description = project_attributes['description']
    image = project_attributes['image']
    # Access profiles data if needed
    profiles = project_attributes['profiles']

    # Create a ProjectLaunch record
    project_launch = ProjectLaunch.find_or_initialize_by(project_id: project_id_value)
    project_launch.update!(
      name: name,
      date: date,
      description: description,
      image: image,
      website: website
    )

    # Iterate over profiles if they exist
    profiles&.each do |profile_data|
      # Access profile attributes
      name = profile_data['name']
      username = profile_data['username']
      avatar_url = profile_data['avatarUrl']
      twitter = profile_data['twitter']
      linkedin = profile_data['linkedin']
      github = profile_data['github']
      websites = profile_data['websites']
      instagram = profile_data['instagram']
      url = profile_data['url']
      
      # Create or update a Profile record associated with the ProjectLaunch
      profile = Profile.find_or_initialize_by(username: username)
      profile.update!(
        name: name,
        avatar_url: avatar_url,
        twitter: twitter,
        linkedin: linkedin,
        github: github,
        websites: websites,
        instagram: instagram,
        url: url,
        project_launch: project_launch
      )
    end
  end
end
