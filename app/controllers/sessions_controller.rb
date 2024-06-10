# app/controllers/sessions_controller.rb
class SessionsController < ApplicationController
    def create
      user = User.from_omniauth(request.env['omniauth.auth'])
      session[:user_id] = user.id
      redirect_to root_path, notice: 'Signed in!'
    end
  
    def destroy
      session[:user_id] = nil
      redirect_to root_path, notice: 'Signed out!'
    end
    def update
        if current_user.update(user_params)
          redirect_to edit_settings_path, notice: 'Settings were successfully updated.'
        else
          render :edit
        end
    end
    def user_params
        params.require(:user).permit(:theme, :notification_preferences)
    end
    def failure
      redirect_to root_path, alert: 'Authentication failed, please try again.'
    end
  end
  