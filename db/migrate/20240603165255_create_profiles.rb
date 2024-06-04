class CreateProfiles < ActiveRecord::Migration[6.1]
  def change
    create_table :profiles do |t|
      t.string :avatar_url
      t.string :name
      t.string :username
      t.string :twitter
      t.string :linkedin
      t.string :github
      t.references :project_launch, foreign_key: true

      t.timestamps
    end
  end
end