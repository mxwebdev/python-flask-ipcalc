# ip-calc-flask

## Install

Create an `instance` folder and a local `config.py` inside the folder.
    ```
    mkdir instance
    nano instance/config.py
    ```

Add local configuration parameters.
    ```python
    SECRET_KEY = 'secretkey'
    ```


## Docker

* docker build -t ipcalcflask:latest .
* docker run --name ipcalcflask -d -p 80:5000 --rm ipcalcflask:latest