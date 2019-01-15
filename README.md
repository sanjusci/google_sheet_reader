# google_sheet_reader
Google Sheet reader and email on given recipients.

> Note: https://developers.google.com/sheets/api/quickstart/python beforehand. 

```
Read Google sheet api authentication and create credentials.json and token.json using google account.
```
### Requirements
Python 3.x, pip3

### How to run?
1. Put SMTP credentials under ```config/base.py```. Other configurations can also be changed but they are optional.
2. Move to ```<project-dir>```, create virtual environment and then activate it as


```sh
$ cd <project-dir>
$ virtualenv -p python3 .env
$ source .env/bin/activate
```


3. Add project to ```PYTHONPATH``` as 

```sh 
$ export PYTHONPATH="$PYTHONPATH:." # . corresponds to current directory(project-dir)
```

3. Under ```<project-dir>``` install requirements/dependencies as 

```sh 
$ pip3 install -r requirements.txt
```

4. Then run reader.py as  

```sh
$ python3  gs_file_reader/reader.py  --sh 1hmTIAOB_5P_1Fn6yi1YteZLr_vP04mgy_6v-KOqKHUI --to  "user1@gmail.com, user2@gmail.com" --cc "user3@gmail.com, user4@gmail.com" --r Sheet1
```
