class CreateUserSessions < ActiveRecord::Migration[7.1]
  def change
    create_table :user_sessions do |t|
      t.integer :user_id
      t.integer :profile_id
      t.string :linkedin
      t.string :linkedin_password
      t.string :linkedin_email

      t.timestamps
    end
  end
end
