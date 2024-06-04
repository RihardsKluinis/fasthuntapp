class Profile < ApplicationRecord
    belongs_to :project_launch
  end
  
  # app/models/project_launch.rb
  class ProjectLaunch < ApplicationRecord
    has_many :profiles
  end