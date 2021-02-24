## Installation
The project requires the following Python packages to be installed (Python 3.6):

* Django
* channels
* channels-redis


All of these are installed via `pip` (or `pip3` if the case), further more, a `requirements.txt` file is provided so install the packages via:

    pip install -r requirements.txt
    
Additionally the following applications are required to enabled channel layer:

* Docker Desktop 

Do not forget to start/enable Docker services. 
To start a Redis server locally on port 6379, run the following command:

    docker run -p 6379:6379 -d redis:5
    
This will enable channel layer that uses Redis as its backing store

## Usage
To start the app (from the project root directory):
    
    python manage.py runserver

Then go to the following url and interact with the application:

    http://localhost:8000

The following directions are available to you:

|                   URL                   
|:---------------------------------------:
| `http://localhost:8000/` 
| `http://localhost:8000/chat/` | Chat Room |
| `http://localhost:8000/login/` | Login form |
| `http://localhost:8000/logout/` | Logout  |
| `http://localhost:8000/create-user/` | Register form |

Firstly, you will ask to Login. you are not enable ti char without an username. So, create a new account to Login. 
When you are logging in, you can type the name room, so you can get a room to chat. After that, you will automatically redirect to a chat room.
 
