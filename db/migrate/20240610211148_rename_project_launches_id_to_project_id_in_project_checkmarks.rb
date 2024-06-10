class RenameProjectLaunchesIdToProjectIdInProjectCheckmarks < ActiveRecord::Migration[7.1]
  def change
    rename_column :project_checkmarks, :project_launches_id, :project_id
  end
end