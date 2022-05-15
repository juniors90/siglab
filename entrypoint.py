# entrypoint.py
# Por ejemplo, APP_SETTINGS_MODULE = config.prod

import os
from backend import create_app

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)

if __name__ == "__main__":
    #if not os.path.exists('db.sqlite'):
    #    db.create_all()
    app.run(debug=True)