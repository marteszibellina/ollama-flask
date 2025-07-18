# Ollama Flask API Chat

_A simple Flask app for Ollama to chat with your model.  
Using terminal is good, but we can do better._

---

## About

The project was created on Flask (a new framework for me, so there may be some bugs).  
Backend took the most time. The framework was adapted from various web projects on GitHub and reworked for my needs.  
The interface is in Russian, but I'm sure you'll handle it.

---

## How to

### _Prerequisites_
1. Download Ollama from the [official website](https://ollama.com/)
2. Choose and download a suitable model from [Ollama library](https://ollama.com/search)

### _Installation_
1. Clone this rep:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```
2. Install Virtual Environment.

    Windows:
    ```bash
    python3 -m venv venv
    venv\Scripts\activate
    ```

    Linux:
    ```bash
    python3.9 -m venv venv
    source venv/bin/activate
    ```

3. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```

4. Configuration

    In routes.py, replace 'gemma3n' with your downloaded model name

    Configure either:

        Edit config.py directly, OR

        Create .env file with:

        # ENV FILE
        FLASK_APP=app  # use it and do not change
        FLASK_ENV=development  # nah
        FLASK_DEBUG=True  # bool

        # DATABASE CONFIGURATION
        SECRET_KEY=your_secret_key  # create yours or use this
        SQLALCHEMY_DATABASE_URI=sqlite:///your_db_name.db  #

5. Database Setup.
    Now you can initialize your DataBase with:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. Running the App
    When it is done, final moves:

    ```bash
    flask run
    ```

    If you've done it right, you will see:

    ```
    * Serving Flask app 'app'
    * Debug mode: on
    WARNING: This is a development server. Do not use it in a production deployment.
    * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
    * Debugger is active!
    * Debugger PIN: ***-***-***
    
    Access the chat interface at http://127.0.0.1:5000
    
# License

    MIT License
