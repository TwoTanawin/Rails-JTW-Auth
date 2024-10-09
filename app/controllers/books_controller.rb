require "jwt"

class BooksController < ApplicationController
  before_action :authorize_request

  def index
    books = [ "Book 1", "Book 2", "Book 3" ]
    render json: books
  end

  private

  SECRET_KEY = Rails.application.credentials.jwt_secret_key

  def authorize_request
    header = request.headers["Authorization"]
    token = header.split(" ").last if header

    begin
      decoded = JWT.decode(token, SECRET_KEY)[0]
      @current_user = User.find(decoded["user_id"])
    rescue ActiveRecord::RecordNotFound, JWT::DecodeError
      render json: { errors: [ "Unauthorized" ] }, status: :unauthorized
    end
  end
end
