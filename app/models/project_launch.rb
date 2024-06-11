class ProjectLaunch < ApplicationRecord
  has_many :profiles
  has_many :project_checkmarks, foreign_key: "project_id"

  scope :with_social_media, ->(social_media) { joins(:profiles).where('profiles.social_media @> ?', "{#{social_media}}") }
  scope :between_dates, ->(start_date, end_date) { where(launch_date: start_date..end_date) }
  scope :with_checkmarks, -> { joins(:project_checkmarks).distinct }
  scope :without_checkmarks, -> { left_joins(:project_checkmarks).where(project_checkmarks: { id: nil }) }
end