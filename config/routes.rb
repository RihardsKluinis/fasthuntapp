Rails.application.routes.draw do
  root "projects#index"
  resources :projects, only: [:index, :show, :edit, :update, :destroy]
  resources :checkmarks, only: [:create, :update]
  resources :project_checkmarks, only: [:create, :update]
  resources :profiles, only: [:show, :edit, :update, :destroy]
  resources :user_sessions, only: [:create]

  devise_for :users, controllers: {
    omniauth_callbacks: 'users/omniauth_callbacks'
  }

  match '/auth/:provider/callback', to: 'users/omniauth_callbacks#google_oauth2', via: [:get, :post]

  get 'auth/:provider/callback', to: 'sessions#create'
  get 'auth/failure', to: redirect('/')

  post 'update_user_sessions', to: 'application_controller#update_user_sessions'
  # Define any other routes here
end