HEROKU = True  # NOTE Make it false if you're not deploying on heroku.

if HEROKU:
    from os import environ
    BOT_TOKEN = environ.get("BOT_TOKEN", None)
    API_ID = int(environ.get("API_ID", 6))
    API_HASH = environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
    SESSION_STRING = environ.get("SESSION_STRING", None)
    MAIN_CHATS = int(environ.get("GBAN_LOG_GROUP_ID", None))
    SUDO_USERS_ID = list(int(x) for x in environ.get("SUDO_USERS_ID", "").split())
    LOG_GROUP_ID = int(environ.get("LOG_GROUP_ID", None))
    GBAN_LOG_GROUP_ID = int(environ.get("MAIN_CHATS", None))
    FERNET_ENCRYPTION_KEY = environ.get("FERNET_ENCRYPTION_KEY", None)
    WELCOME_DELAY_KICK_SEC = int(environ.get("WELCOME_DELAY_KICK_SEC", None))
    MONGO_DB_URI = environ.get("MONGO_DB_URI", None)
    ARQ_API_BASE_URL = environ.get("ARQ_API_BASE_URL", None)

if not HEROKU:
    BOT_TOKEN = "467677575:YZfaakjwd545dfg-N6JStihhuw5gQeZHntc"
    API_ID = 123456
    API_HASH = "dfxcgs5s12hdcxfgdfz"
    PHONE_NUMBER = "+919425965543" # Need for Helper Userbot
    MAIN_CHATS = [-100125431255]  # NOTE These are the chats where main functions of bot will work, like music downloading etc.
    SUDO_USERS_ID = [4543744343, 543214651351] # Sudo users have full access to everythin, don't trust anyone
    LOG_GROUP_ID = -100125431255
    GBAN_LOG_GROUP_ID = -100125431255
    FERNET_ENCRYPTION_KEY = "iKMq0WZMnJKjMQxZWKtv-cplMuF_LoyshXj0XbTGGWM=" # Leave this as it is
    WELCOME_DELAY_KICK_SEC = 300
    MONGO_DB_URI = "mongodb+srv://username:password@cluster0.ksiis.mongodb.net/YourDataBaseName?retryWrites=true&w=majority"

    # NOTE Don't make changes below this line
    ARQ_API_BASE_URL = "http://thearq.tech"
