class CheckmarksController < ApplicationController
    before_action :authenticate_user!
  
    def create
        Rails.logger.info("Checkmark for user #{current_user.id}, project #{params[:project_id]}, profile #{params[:profile_id]}CREATE successfully.")
        profile = Profile.find(params[:checkmark][:profile_id])
        # Create a new checkmark associated with the current user and the profile
        checkmark = current_user.checkmarks.new(profile: profile, checked: params[:checkmark][:checked])
        if checkmark.save
          render json: { success: true }
        else
          render json: { errors: checkmark.errors }, status: :unprocessable_entity
        end
    end
  
    def update
      @checkmark = current_user.checkmarks.find(params[:id])
      Rails.logger.info("Checkmark for user #{current_user.id}, project #{params[:project_id]}, profile #{params[:profile_id]}NOT updated successfully.")
      if @checkmark.update(checkmark_params)
        Rails.logger.info("Checkmark for user #{current_user.id}, project #{params[:project_id]}, profile #{params[:profile_id]} updated successfully.")
        render json: @checkmark, status: :ok
      else
        render json: @checkmark.errors, status: :unprocessable_entity
      end
    end
  
    private
  
    def checkmark_params
      params.require(:checkmark).permit(:profile_id, :checked)
    end
  end
  