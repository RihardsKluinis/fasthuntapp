class AddIsThisPasswordCorrectToUserSessions < ActiveRecord::Migration[7.1]
  def change
    add_column :user_sessions, :is_this_password_correct, :boolean
  end
end
