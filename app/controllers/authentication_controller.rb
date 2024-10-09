class AuthenticationController < ApplicationController
  # Skip CSRF token verification for API endpoints like signup and login
  skip_before_action :verify_authenticity_token, only: [ :signup, :login ]

  SECRET_KEY = Rails.application.credentials.jwt_secret_key

  def signup
    user = User.new(user_params)
    if user.save
      token = encode_token(user_id: user.id)
      render json: { user: user, token: token }, status: :created
    else
      render json: { errors: user.errors.full_messages }, status: :unprocessable_entity
    end
  end

  def login
    user = User.find_by(username: params[:username])
    if user&.authenticate(params[:password])
      token = encode_token(user_id: user.id)
      render json: { user: user, token: token }, status: :ok
    else
      render json: { errors: [ "Invalid username or password" ] }, status: :unauthorized
    end
  end

  private

  def encode_token(payload)
    JWT.encode(payload, SECRET_KEY)
  end

  def user_params
    params.permit(:username, :password)
  end
end
