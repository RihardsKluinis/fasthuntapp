class CreateCheckmarks < ActiveRecord::Migration[7.1]
  def change
    create_table :checkmarks do |t|
      t.references :user, null: false, foreign_key: true
      t.references :profile, null: false, foreign_key: true
      t.boolean :checked

      t.timestamps
    end
  end
end
