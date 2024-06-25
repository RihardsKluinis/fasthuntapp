Rails.application.routes.draw do
  root "projects#index"
  resources :projects, only: [:index, :show, :edit, :update, :destroy]

  post 'update_user_session', to: 'application#update_user_session'
  # Define any other routes here
end