class UserSessionsController < ApplicationController
    protect_from_forgery with: :null_session # Adjust CSRF protection as needed
  
    def create
      session_data = user_session_params
  
      @user_session = UserSession.new(session_data)
  
      if @user_session.save
        render json: { message: 'User session created successfully' }, status: :created
      else
        render json: { errors: @user_session.errors.full_messages }, status: :unprocessable_entity
      end
    end
  
    private
  
    def user_session_params
      params.require(:user_session).permit(:user_id, :profile_id, :linkedin, :linkedin_password, :linkedin_email)
    end
  end
  