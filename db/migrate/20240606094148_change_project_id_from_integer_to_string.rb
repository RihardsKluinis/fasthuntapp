class ChangeProjectIdFromIntegerToString < ActiveRecord::Migration[7.1]
  def change 
    change_column :project_launches, :project_id, :string
  end
end
