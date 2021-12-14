### How do I get set up a script?(Tested on Ubuntu) ###

* Update and install package
    ```
    apt-get update
    apt install git  -y
    apt install curl -y
    apt-get install -yq python3-pip
    ```
* Goto download folder
    ```
    git clone https://github.com/d3folt-cmd/yalantis_test.git
    cd yalantis_test
    ```
* Install virtual env:
    ```bash
    pip3 install virtualenv
    virtualenv venv
    source venv/bin/activate
    ```
* Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```
* Create db
    ```
    python3 create_db/create.py
    ```
* Run app.py script:  
    ```bash
    python3 app.py
    ```
