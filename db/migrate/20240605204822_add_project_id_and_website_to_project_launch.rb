class AddProjectIdAndWebsiteToProjectLaunch < ActiveRecord::Migration[7.1]
  def change
    add_column :project_launches, :project_id, :integer
    add_column :project_launches, :website, :string
  end
end
