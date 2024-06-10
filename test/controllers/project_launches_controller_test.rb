require "test_helper"

class ProjectLaunchesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @project_launch = project_launches(:one)
  end

  test "should get index" do
    get project_launches_url
    assert_response :success
  end

  test "should get new" do
    get new_project_launch_url
    assert_response :success
  end

  test "should create project_launch" do
    assert_difference("ProjectLaunch.count") do
      post project_launches_url, params: { project_launch: { date: @project_launch.date, description: @project_launch.description, image: @project_launch.image, name: @project_launch.name } }
    end

    assert_redirected_to project_launch_url(ProjectLaunch.last)
  end

  test "should show project_launch" do
    get project_launch_url(@project_launch)
    assert_response :success
  end

  test "should get edit" do
    get edit_project_launch_url(@project_launch)
    assert_response :success
  end

  test "should update project_launch" do
    patch project_launch_url(@project_launch), params: { project_launch: { date: @project_launch.date, description: @project_launch.description, image: @project_launch.image, name: @project_launch.name } }
    assert_redirected_to project_launch_url(@project_launch)
  end

  test "should destroy project_launch" do
    assert_difference("ProjectLaunch.count", -1) do
      delete project_launch_url(@project_launch)
    end

    assert_redirected_to project_launches_url
  end
end
