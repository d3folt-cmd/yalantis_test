### What is this repository for? ###

* Test task for Yalantis school on Pyhton using Flask, SQLite

### How do I get set up a script? ###

* Clone repository
* Goto download folder
* Install virtual env:
    ```bash
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    ```
* Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
* Run app.py script:  
    ```bash
    python app.py
    ```

### Design description

In file create.py run method create() that contains several methods:

create.db() - method from create_database.py that creates tables empty 'driver' and 'vehicle'.

clear.db() - method from create_database.py clears all data from tables so it is easier to create tables with new data again.

adddata() - method from add_data.py that fills tables with data you write here.

displaydata() - display tables in console.

Run app.py to run the project.

After running app.py you can run test.py where are two simple test methods - first add driver and second print his id.
