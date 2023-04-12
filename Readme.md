# Go Beta Ride Booking Service

This is a backend project for a car ride booking service using Python and FastAPI.

## Installation

Clone the repository:

git clone <https://github.com/joel-danjuma/Go_beta.git>
cd Go_beta
Install the dependencies:

pip install -r requirements.txt

Run the server:
uvicorn main:app --reload
The server should now be running at `http://localhost:8000`.

## API Endpoints

The following endpoints are available:

/: Root page for the API.
/posts: CRUD operations for posts.
/users: CRUD operations for users.
/auth: Authentication and authorization endpoints.
/providers: CRUD operations for service providers.

## Authentication

Authentication is required for most endpoints. To authenticate, send a POST request to /auth/token with the following JSON payload:
"username": "your-username",
"password": "your-password"

The response will contain an access token that should be included in the Authorization header of all subsequent requests:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Thanks for checking out our car ride booking service! If you have any questions or issues, please feel free to contact us.
