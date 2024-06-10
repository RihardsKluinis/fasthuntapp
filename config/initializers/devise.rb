Devise.setup do |config|
    # Other Devise configurations...
  
    config.mailer_sender = 'chiganskis@gmail.com'
    require 'devise/orm/active_record'
    config.case_insensitive_keys = [:email]
    config.strip_whitespace_keys = [:email]
    config.skip_session_storage = [:http_auth]
    config.stretches = Rails.env.test? ? 1 : 12
    config.reconfirmable = true
    config.expire_all_remember_me_on_sign_out = true
    config.password_length = 6..128
    config.email_regexp = /\A[^@\s]+@[^@\s]+\z/
    config.reset_password_within = 6.hours
    config.sign_out_via = :delete
    config.responder.error_status = :unprocessable_entity
    config.responder.redirect_status = :see_other


    #config.omniauth :github, ENV['GITHUB_CLIENT_ID'], ENV['GITHUB_CLIENT_SECRET'], scope: 'user,public_repo'
    config.omniauth :github, ENV['GITHUB_CLIENT_ID']'Ov23li7X2ZrQZXGLolLt', ENV['GITHUB_CLIENT_SECRET']'b637b95cdbec8cd764068b18bf9c506b817c0af4', scope: 'user,public_repo'

    config.omniauth :google_oauth2, ENV['GOOGLE_CLIENT_ID'], ENV['GOOGLE_CLIENT_SECRET'], {

        }

    OmniAuth.config.allowed_request_methods = [:get, :post]
    OmniAuth.config.silence_get_warning = true
        

  end
