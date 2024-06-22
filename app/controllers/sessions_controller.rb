class SessionsController < ApplicationController
  def create
    user = User.from_omniauth(request.env['omniauth.auth'])
    session[:user_id] = user.id
    
    if user.user_sessions.exists?(is_this_password_correct: false)
      flash[:alert] = "There is an incorrect password attempt in your history."
    end

    redirect_to root_path, notice: 'Signed in!'
  end

  def destroy
    # Adjusted for Devise if needed, otherwise remove `super`
    super do
      return redirect_to after_sign_out_path_for(resource_name), status: :see_other
    end
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
