# Flask AI Gen API
This API allows generating text from a prompt provided by the user, using the GPT-2 model. This API includes functionalities such as requesting a text generation through a provided text, request history, basic authentication and configuring the model parameters.

# Features

 - JWT Authentication: Secure endpoints with JSON Web Tokens.
 - AI-Generated Responses: Generate text using the GPT-2 model.
 - Configurable Parameters: Customize model behavior (e.g., max_length, temperature, top_k, top_p).
 - Conversation History: Retrieve previous interactions with the AI

## Requirements

 - Python 3.12.8
 - Dependencies: Listed in requirements.txt

# Install (using docker)

By default, docker is configured to run the API on port 5000. If you want to change the port, you can modify the `docker-compose.yml` file.
Guincorn is used as the WSGI server, and the number of workers is set to 4. You can modify this configuration in the `Dockerfile`.

```bash
docker-compose build
docker-compose up
```

# Install (without docker)

1. Clone repository: 
```bash
git clone https://github.com/aleeeesf/Flask-Gen-AI-API
cd Flask-Gen-AI-API
```

2. Create a virtual environment:
```bash
python -m venv venv 
source venv/bin/activate 
# On Windows: .\venv\Scripts\activate
```

3. Install Dependecies:
```bash
pip install -r requirements.txt
```

4. Execute:
```bash
python app.py
```

## Default Port

By default, the application runs on port 5000. You can access the API at:

```bash
http://localhost:5000
```

If you want to change the port, you can modify the app.run() line in app.py:

```python
app.run(debug=False, host="0.0.0.0", port=<your_custom_port>)
```

Alternatively, if you're using Docker, you can update the docker-compose.yml file to map a different host port:

```yaml
services:
  flask_app:
    ports:
      - "<your_custom_port>:5000"
```

## Documentation with Postman

The API is documented interactively using **Postman**. You can access the documentation at the following URL:

https://documenter.getpostman.com/view/20405699/2sAYQghUK6

## Security

To access the endpoints, authentication via **JWT** is required. The token must be sent in the request header in the format `Authorization: Bearer <token>`.
