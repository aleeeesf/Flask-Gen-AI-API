# Flask AI Gen API
This API allows generating text from a prompt provided by the user, using the GPT-2 model. This API includes functionalities such as requesting a text generation through a provided text, request history, basic authentication and configuring the model parameters.

# Features

 - Authentication through JWT (JSON Web Tokens).
 - Sending messages through a RESTful endpoint.
 - Responses generated by the AI model.
 - Access to conversation history.

## Requirements

-   Python 3.12.8

# Install (using docker)

    ``docker-compose build
     docker-compose up``

# Install (without docker)

 1. Clone repository: 
 ``git clone https://github.com/tu_usuario/chat-api.git
cd chat-api``
 2. Create a virtual environment:
 ``python -m venv venv 
  source venv/bin/activate # On Windows: venv\Scripts\activate``
 3. Install Dependecies:
 ``pip install -r requirements.txt``
 4. Execute:
 ``python app.py``

## Documentation with Postman

The API is documented interactively using **Postman**. You can access the documentation at the following URL:

https://documenter.getpostman.com/view/20405699/2sAYQghUK6

## Security

To access the endpoints, authentication via **JWT** is required. The token must be sent in the request header in the format `Authorization: Bearer <token>`.
