class AddUniqueIdentifierToProjects < ActiveRecord::Migration[7.1]
  def change
    add_column :project_launches, :unique_identifier, :string
    add_index :project_launches, :unique_identifier, unique: true
  end
end
