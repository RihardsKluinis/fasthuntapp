class AddWebsitesAndInstagramToProfiles < ActiveRecord::Migration[7.1]
  def change
    add_column :profiles, :websites, :string
    add_column :profiles, :instagram, :string
  end
end
