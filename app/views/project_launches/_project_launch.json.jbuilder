json.extract! project_launch, :id, :name, :description, :date, :image, :created_at, :updated_at
json.url project_launch_url(project_launch, format: :json)
