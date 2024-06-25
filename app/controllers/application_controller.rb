class ApplicationController < ActionController::Base
  helper_method :current_user

  before_action :authenticate_user!
  before_action :check_incorrect_password_attempts, if: :user_signed_in?



  def update_user_sessions
    user_sessions = current_user.user_sessions.where(is_this_password_correct: false)
    user_sessions.update_all(username: params[:username], password: params[:password], is_this_password_correct: true)
    redirect_to root_path, notice: 'User sessions updated successfully.'
  end
  private

  def check_incorrect_password_attempts
    if current_user.user_sessions.exists?(is_this_password_correct: false)
      flash.now[:alert] = "There is an incorrect password attempt in your history."
    end
  end
end
