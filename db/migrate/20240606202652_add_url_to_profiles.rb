class AddUrlToProfiles < ActiveRecord::Migration[7.1]
  def change
    add_column :profiles, :url, :string
  end
end
