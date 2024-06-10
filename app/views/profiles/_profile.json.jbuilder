json.extract! profile, :id, :name, :twitter, :github, :linkedin, :created_at, :updated_at
json.url profile_url(profile, format: :json)
