class CreateProjectLaunches < ActiveRecord::Migration[7.1]
  def change
    create_table :project_launches do |t|
      t.string :name
      t.text :description
      t.datetime :date
      t.string :image

      t.timestamps
    end
  end
end
