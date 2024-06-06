# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.1].define(version: 2024_06_06_202652) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "profiles", force: :cascade do |t|
    t.string "avatar_url"
    t.string "name"
    t.string "username"
    t.string "twitter"
    t.string "linkedin"
    t.string "github"
    t.bigint "project_launch_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "websites"
    t.string "instagram"
    t.string "url"
    t.index ["project_launch_id"], name: "index_profiles_on_project_launch_id"
  end

  create_table "project_launches", force: :cascade do |t|
    t.string "name"
    t.text "description"
    t.datetime "date"
    t.string "image"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "project_id"
    t.string "website"
  end

  add_foreign_key "profiles", "project_launches"
end
