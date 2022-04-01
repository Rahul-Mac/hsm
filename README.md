# Hardware Service Manager
This software is used to store complaints of hardware related issues and write a remark after servicing the devices.
![Screenshot](image.png)
# How To Use
* Download the source code
* Install the dependencies
  ```
    pip install PyQt5
    pip install pandas
    pip install mysql-connector-python
  ```
* Create a database named `servicemgmt`
* Execute all the queries in the [sql file](https://github.com/Rahul-Mac/hsm/blob/main/db_file.sql)
* Replace all occurences of `GMIT.LHDOMAIN.LOCAL` to the name of your MySQL host in the source code files.
* Run
  ```
    python main.py
  ```
