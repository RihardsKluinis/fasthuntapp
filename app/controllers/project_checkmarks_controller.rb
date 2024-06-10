class ProjectCheckmarksController < ApplicationController
    before_action :authenticate_user!
  
    def create
        project_checkmark = current_user.project_checkmarks.find_by(project_id: params[:project_checkmark][:project_id])
        
        if project_checkmark
          project_checkmark.update(checked: params[:project_checkmark][:checked])
          render json: { success: true }
        else
          project_checkmark = current_user.project_checkmarks.new(project_checkmark_params)
          if project_checkmark.save
            render json: { success: true }
          else
            render json: { errors: project_checkmark.errors.full_messages }, status: :unprocessable_entity
          end
        end
      end
      
  
    def update
      @project_checkmark = current_user.project_checkmarks.find_by(project_id: params[:project_id])
      if @project_checkmark.update(project_checkmark_params)
        render json: { success: true }
      else
        render json: { success: false, errors: @project_checkmark.errors.full_messages }, status: :unprocessable_entity
      end
    end
  
    private
  
    def project_checkmark_params
      params.require(:project_checkmark).permit(:project_id, :checked)
    end
  end
  