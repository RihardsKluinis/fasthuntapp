class CreateUserSessions < ActiveRecord::Migration[7.1]
  def change
    create_table :user_sessions do |t|
      t.text :action
      t.string :status

      t.timestamps
    end
  end
end
