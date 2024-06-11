# app/models/user.rb
class User < ApplicationRecord
    # Include default devise modules. Others available are:
    # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable

    has_many :checkmarks, dependent: :destroy
    has_many :checked_profiles, through: :checkmarks, source: :profile

    has_many :project_checkmarks
    has_many :project_launches, through: :project_checkmarks

    devise :database_authenticatable, :registerable,
           :recoverable, :rememberable, :validatable,
           :omniauthable, omniauth_providers: [:google_oauth2, :github]
  
    # Associations
    has_many :checkmarks, dependent: :destroy
    has_many :checked_profiles, through: :checkmarks, source: :profile
    
    has_many :project_checkmarks, dependent: :destroy
    has_many :checked_projects, through: :project_checkmarks, source: :project_launch
  
    # Validations
    validates :email, presence: true, uniqueness: true
    validates :provider, presence: true, unless: -> { uid.blank? }
    validates :uid, presence: true, uniqueness: { scope: :provider }, unless: -> { uid.blank? }
  
    # Store settings as a JSONB column
    store_accessor :settings, :theme, :notification_preferences
  
    # Skip password validation for users created via OAuth
    def password_required?
      super && provider.blank?
    end
  
    # Find or create a user from OAuth data
    def self.from_omniauth(auth)
      where(provider: auth.provider, uid: auth.uid).first_or_initialize.tap do |user|
        user.email = auth.info.email
        user.name = auth.info.name
        user.password = Devise.friendly_token[0, 20] if user.new_record?
        user.save(validate: false) # Skip validations for user creation via OAuth
      end
    end
  end
  