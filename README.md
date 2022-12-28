## College-Chatbot API 

## Abstract
During the admissions process or for other reasons, students frequently need to visit universities or schools to gather information about numerous topics such tuition costs, term schedules, etc. A chatbot can be created as a result to solve the issues. The idea focusses upon user-chatbot interaction, which can be accessible from anywhere at any time. The project makes use of machine learning and artificial intelligence. A Feed-Forward PyTorch Neural Network with two layers, ReLU activation, and Cross-Entropy Loss is used to optimize the parameters in chatbot model. To rapidly exchange messages between the client and server, a socket connection is essential. This is due to the fact that a straightforward HTTP connection cannot guarantee real-time, bidirectional communication between the client and the server. For the chatbot API, the project will utilize FastAPI since it offers a quick and up-to-date Python server for our purpose and MongoDB for storing model state and datasets. The mobile application is developed using React-Native and built via Expo Application Services, only android devices are supported. In addition, there is a Web Application that acts as admin interface for the Chatbot API which is implemented using React JS.

## Dependency
- Use version python 3.10.+
- Use stable version PyTorch 

## Running in development environment

### Clone the application
```
git clone https://github.com/jhonas-palad/Chatbot-API.git
cd Chatbot-API
```

### Create virtual environment
```
python -m venv venv

#bash
source ./venv/bin/activate

#pwsh
./venv/scripts/activate

```

### Install dependencies
```
pip install -r requirements.txt
```

### Create an .env file
Enironment variables:
 - DATABASE_URL - MongoDB connection
 - ACCESS_TOKEN_EXPIRE_MINUTES - Access token time expiration in minutes
 - REFRESH_TOKEN_EXPIRE_MINUTES - Refresh token time expiration in minutes
 - ALGORITHM - Algorithm to used for signing the tokens. String
 - JWT_SECRET_KEY: Any string
 - JWT_REFRESH_SECRET_KEY: Any string
 - SECRET_PASS - Any string that will be used to register a user


### Run the application
```
uvicorn app:app --reload
```


Visit docs: https://chatbotapi.site/docs

Mobile application source https://github.com/jhonas-palad/Chatbot-MobileApp.git

Web application source : https://github.com/jhonas-palad/Chatbot-Admin.git
