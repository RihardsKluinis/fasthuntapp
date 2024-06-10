class Profile < ApplicationRecord
    belongs_to :project_launch
    has_many :checkmarks, dependent: :destroy
    has_many :checked_by_users, through: :checkmarks, source: :user
end