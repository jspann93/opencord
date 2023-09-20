In order to build: 
    1. Install NPM (https://nodejs.org/dist/v18.17.1/node-v18.17.1-x64.msi)

    2. In terminal/cmd of working directory enter the command: npm install 

    3. To start the application in terminal/cmd enter the command: npm start


To ensure all modules/libraries are the same version create a Python virtual environment with this command in your cmd/terminal: 

    python -m venv /path/to/new/virtual/environment


To activate the virtual environment on Windows in powershell/cmd enter the command: 
    <venv>\Scripts\activate

To activate the virtual environment on Mac in terminal enter: 
    source venv/bin/activate

Once activated to the far left in your terminal/cmd it should have the name of the virtual environment. 

To install the required libraries/modules in the venv enter the command: 

    pip install -r requirements.txt 


requirements.txt is included in the git files. 


To run flask server:
    While in the webserver directory in terminal/cmd enter the command:

        flask --app main run

To access the web server pages in browser go to the url: 

    http://127.0.0.1:5000