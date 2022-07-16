from website import create_app
from website import form_contact
import numpy as np
import os

if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run()
