class ProjectCheckmarksController < ApplicationController
    before_action :authenticate_user!
  
    def create
      project_checkmark = current_user.project_checkmarks.find_or_initialize_by(project_id: params[:project_checkmark][:project_id])
      project_checkmark.checked = params[:project_checkmark][:checked]
  
      if project_checkmark.save
        update_profile_checkmarks(project_checkmark.project_id, project_checkmark.checked)
        render json: { success: true }
      else
        render json: { errors: project_checkmark.errors }, status: :unprocessable_entity
      end
    end
  
    def update
      project_checkmark = current_user.project_checkmarks.find(params[:id])
  
      if project_checkmark.update(project_checkmark_params)
        update_profile_checkmarks(project_checkmark.project_id, project_checkmark.checked)
        render json: project_checkmark, status: :ok
      else
        render json: project_checkmark.errors, status: :unprocessable_entity
      end
    end
  
    private
  
    def project_checkmark_params
      params.require(:project_checkmark).permit(:project_id, :checked)
    end
  
    def update_profile_checkmarks(project_id, checked)
      begin
        project = ProjectLaunch.find(project_id)
      rescue ActiveRecord::RecordNotFound => e
        Rails.logger.error("Project not found: #{e.message}")
        return
      end
  
      profiles = project.profiles
      profiles.each do |profile|
        checkmark = current_user.checkmarks.find_or_initialize_by(profile_id: profile.id)
        checkmark.checked = checked
        checkmark.save
      end
    end
  end
  