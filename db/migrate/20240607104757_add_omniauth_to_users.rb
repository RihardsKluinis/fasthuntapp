class AddOmniauthToUsers < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :image, :string
  end
end
