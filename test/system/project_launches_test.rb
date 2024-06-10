require "application_system_test_case"

class ProjectLaunchesTest < ApplicationSystemTestCase
  setup do
    @project_launch = project_launches(:one)
  end

  test "visiting the index" do
    visit project_launches_url
    assert_selector "h1", text: "Project launches"
  end

  test "should create project launch" do
    visit project_launches_url
    click_on "New project launch"

    fill_in "Date", with: @project_launch.date
    fill_in "Description", with: @project_launch.description
    fill_in "Image", with: @project_launch.image
    fill_in "Name", with: @project_launch.name
    click_on "Create Project launch"

    assert_text "Project launch was successfully created"
    click_on "Back"
  end

  test "should update Project launch" do
    visit project_launch_url(@project_launch)
    click_on "Edit this project launch", match: :first

    fill_in "Date", with: @project_launch.date
    fill_in "Description", with: @project_launch.description
    fill_in "Image", with: @project_launch.image
    fill_in "Name", with: @project_launch.name
    click_on "Update Project launch"

    assert_text "Project launch was successfully updated"
    click_on "Back"
  end

  test "should destroy Project launch" do
    visit project_launch_url(@project_launch)
    click_on "Destroy this project launch", match: :first

    assert_text "Project launch was successfully destroyed"
  end
end
