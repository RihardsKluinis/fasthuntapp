class CheckmarksController < ApplicationController
    before_action :authenticate_user!
  
    def create
      profile = Profile.find(params[:checkmark][:profile_id])
      checkmark = current_user.checkmarks.new(profile: profile, checked: params[:checkmark][:checked])
  
      if checkmark.save
        update_project_checkmark_if_all_profiles_checked(profile.project_launch)
        render json: { success: true, id: checkmark.id }
      else
        render json: { errors: checkmark.errors }, status: :unprocessable_entity
      end
    end
  
    def update
      checkmark = current_user.checkmarks.find(params[:id])
  
      if checkmark.update(checkmark_params)
        update_project_checkmark_if_all_profiles_checked(checkmark.profile.project_launch)
        render json: checkmark, status: :ok
      else
        render json: checkmark.errors, status: :unprocessable_entity
      end
    end
  
    private
  
    def checkmark_params
      params.require(:checkmark).permit(:profile_id, :checked)
    end
  
    def update_project_checkmark_if_all_profiles_checked(project_launch)
      all_checked = project_launch.profiles.all? do |profile|
        current_user.checkmarks.exists?(profile_id: profile.id, checked: true)
      end
  
      project_checkmark = current_user.project_checkmarks.find_or_initialize_by(project_id: project_launch.id)
      project_checkmark.checked = all_checked
      project_checkmark.save
    end
  end
  