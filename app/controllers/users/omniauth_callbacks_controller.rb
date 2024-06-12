class Users::OmniauthCallbacksController < Devise::OmniauthCallbacksController
    def google_oauth2
      handle_auth "Google"
    end
  
    def github
      handle_auth "GitHub"
    end
  
    def failure
      Rails.logger.debug "OmniAuth failure: #{params[:message]}"
      redirect_to root_path
      super
    end
  
    private
  
    def handle_auth(kind)
        auth = request.env['omniauth.auth']
        Rails.logger.debug "Auth data: #{auth.inspect}"
        
        @user = User.from_omniauth(auth)
        if @user.persisted?
          sign_in_and_redirect @user, event: :authentication
          set_flash_message(:notice, :success, kind: kind) if is_navigational_format?
        else
          Rails.logger.debug "User creation failed: #{@user.errors.full_messages.join("\n")}"
          session["devise.#{kind.downcase}_data"] = auth.except("extra")
          flash[:alert] = "There was a problem signing you in through #{kind}. Please register or try again."
          redirect_to new_user_registration_url
        end
      end
  end
  