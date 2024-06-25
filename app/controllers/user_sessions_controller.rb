class UserSessionsController < ApplicationController
    protect_from_forgery with: :null_session # Adjust CSRF protection as needed
  
    def create
      session_data = user_session_params
      Rails.logger.info("Received parameters: #{session_data.inspect}")
      @user_session = UserSession.new(session_data)
      @user_session.user_id = current_user.id
      if @user_session.save
        render json: { message: 'User session created successfully' }, status: :created
      else
        render json: { errors: @user_session.errors.full_messages }, status: :unprocessable_entity
      end
    end
  
    private
  
    def user_session_params
      params.require(:user_session).permit(:profile_id, :user_id, :linkedin_password, :linkedin_email, :linkedin)
    end

    def update_user_sessions
        user_sessions = current_user.user_sessions.where(is_this_password_correct: false)
        user_sessions.update_all(username: params[:username], password: params[:password], is_this_password_correct: true)
        redirect_to root_path, notice: 'User sessions updated successfully.'
      end
  end
  