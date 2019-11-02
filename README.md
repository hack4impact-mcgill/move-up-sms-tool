# Move Up - SMS Tool

This project will allow potential clients to sign up for [Move Up's](http://www.moveuptoday.org/) services by texting a dedicated hotline.  

## Development Team

**Project Manager:** Albert Kragl

**Developers:** Alana Ceci, Alex Lam, Jonathan Colaco Carr, Kira Noël, Madonna Huang, Nafiz Islam, Tom Wright, Xin Rui Li, Yasasa Abey

## Setup and Installation

To get the backend set up, follow the instructions in the `README` in the `backend` folder.

Running the backend requires having some environment variables defined. To do this, create a file called `.env` at the root of the `backend` folder, and define variables in the following format:

```
EXAMPLE_VAR=example_value
SECRET_VAR=supersecretpassword
```

You will need to define values for `FLASK_CONFIG` (can be either `development`, `testing` or `production`),  `TWILIO_AUTH_TOKEN` (auth token for your Twilio account) and `TWILIO_ACCOUNT_SID` (SID for your Twilio account). Once this file is created with proper values, the app will automatically load them into the environment when run. To use these environment variables, you can do the following in your code:

```
import os

# get the value of the TWILIO_AUTH_TOKEN environment variable
env_var = os.environ.get("TWILIO_AUTH_TOKEN")
```

 