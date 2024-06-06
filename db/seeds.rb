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

file = File.read(Rails.root.join('db', 'data', 'projects.json'))
json_data = JSON.parse(file)

# Iterate over each project
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
  project_launch = ProjectLaunch.create!(
                                        name: name,
                                        date: date,
                                        description: description,
                                        image: image,
                                        website: website,
                                        project_id: project_id_value # Assign project_id from JSON data directly
                                        )

  # Iterate over profiles if they exist
  if profiles
    profiles.each do |profile_id, profile_data|
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
      
      # Create a Profile record associated with the ProjectLaunch
      Profile.create!(
        name: name,
        username: username,
        avatar_url: avatar_url,
        twitter: twitter,
        linkedin: linkedin,
        github: github,
        websites: websites,
        instagram: instagram,
        project_launch: project_launch,
        url: url
      )
    end
  end
end
