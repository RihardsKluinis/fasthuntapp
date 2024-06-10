class ProjectCheckmark < ApplicationRecord
  belongs_to :user
  belongs_to :project_launch, foreign_key: "project_id"

  validates :user_id, uniqueness: { scope: :project_id }
end