class RemoveUniqueIdentifierFromProjectLaunches < ActiveRecord::Migration[7.1]
  def change
    remove_index :project_launches, :unique_identifier
    remove_column :project_launches, :unique_identifier, :string
  end
end
