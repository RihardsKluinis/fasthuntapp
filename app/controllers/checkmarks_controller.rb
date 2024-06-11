class CheckmarksController < ApplicationController
    before_action :authenticate_user!
  
    def create
      profile = Profile.find(params[:checkmark][:profile_id])
      checkmark = current_user.checkmarks.find_or_initialize_by(profile: profile)
      checkmark.checked = params[:checkmark][:checked]
  
      if checkmark.save
        render json: { success: true, id: checkmark.id }
      else
        render json: { errors: checkmark.errors }, status: :unprocessable_entity
      end
    end
  
    def update
      checkmark = current_user.checkmarks.find(params[:id])
  
      if checkmark.update(checkmark_params)
        render json: { success: true }
      else
        render json: { errors: checkmark.errors }, status: :unprocessable_entity
      end
    end
  
    private
  
    def checkmark_params
      params.require(:checkmark).permit(:profile_id, :checked)
    end
  end
  