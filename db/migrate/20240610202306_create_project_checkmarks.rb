class CreateProjectCheckmarks < ActiveRecord::Migration[6.1]
  def change
    create_table :project_checkmarks do |t|
      t.references :user, null: false, foreign_key: true
      t.references :project_launches, null: false, foreign_key: true
      t.boolean :checked, default: false

      t.timestamps
    end
  end
end