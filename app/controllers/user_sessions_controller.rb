class UserSessionsController < ApplicationController
    protect_from_forgery with: :null_session # Ensure CSRF protection is adjusted as needed
  
    # POST /user_sessions
    def create
      session_data = user_session_params
  
      # Assuming you want to save the session data to the database
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