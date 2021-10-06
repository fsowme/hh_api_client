# HH API-client
Pet-project. Sends new vacancies to telegram from hh.

## How to use
1. Create and save new vacancy search with required parameters.
2. Start conversation with telegram bot "fsow_hh", register and login with hh account.
3. Make sure you are subscribed to the new vacancy search in the bot menu or in hh application.
4. You will receive new vacancies (Check interval is 5 minutes).
5. Profit!

## Plans for the future
* Site with statistics of responses/invitations with information about stages of interviews (hr, test, teamlead...)
* Change notification intervals for each vacancy search
* Use redis as message broker for notifications


## Requirements

* Register a new app in dev.hh.ru.

* Register a telegram bot.

* Docker and docker-compose must be installed in your system. More information you can take on official site of Docker.
    ([docker](https://docs.docker.com/engine/install/),
    [docker-compose](https://docs.docker.com/compose/install/))

* .env file example:

    ```
    FLASK_SECRET_KEY="KEY"
    REDIRECT_URL=""
    HH_BASE_URL="https://hh.ru"
    HH_BASE_API_URL="https://api.hh.ru"
    REG_URL_PATH="/oauth/authorize"
    TOKEN_URL_PATH="/oauth/token"
    AUTOSEARCHES_PATH="/saved_searches/vacancies"
    VACANCIES_PATH="/vacancies"
    GRANT_TYPE_CODE="authorization_code"
    GRANT_TYPE_REFRESH="refresh_token"
    GRANT_TYPE_CC="client_credentials"
    CLIENT_ID="" # Search in your account on dev.hh.ru
    CLIENT_SECRET="" # Search in your account on dev.hh.ru

    #Telegram
    TG_TOKEN=""
    PERSISTENCE="persist.bin"

    #PSQL
    DB_HOST="localhost"
    DB_PORT="5432"
    POSTGRES_USER="postgres"
    POSTGRES_PASSWORD="postgres"
    POSTGRES_DB="db_name"

    ```

## Built with

* [Flask](https://flask.palletsprojects.com) - The web framework used
* [Python telegram bot](https://github.com/python-telegram-bot/python-telegram-bot) - Python telegram bot


## Author

* **Vitalii Mikhailov**

