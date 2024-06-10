Rails.application.routes.draw do
  root "projects#index"
  resources :projects, only: [:index, :show, :edit, :update, :destroy]
  resources :checkmarks, only: [:create, :update]
  resources :profiles, only: [:show, :edit, :update, :destroy]
  devise_for :users, controllers: {
    omniauth_callbacks: 'users/omniauth_callbacks'
  }
  match '/auth/:provider/callback', to: 'users/omniauth_callbacks#google_oauth2', via: [:get, :post]

  get 'auth/:provider/callback', to: 'sessions#create'
  get 'auth/failure', to: redirect('/')
  get 'signout', to: 'sessions#destroy', as: 'signout'

  # Define any other routes here
end