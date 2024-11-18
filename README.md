# CacheMock
A very simple mock server. It will query another server, and then, on the same URL, reply with the same stuff.

### Install
_Best inside a virtualenv_
```shell
pip install -r requirements.txt
```

### Usage

```
python app.py
```
Now open [https://localhost:5000/__proxy__](https://localhost:5000/__proxy__).  
There you can set the URL where to proxy to.  
Additionally, you can review the made requests.  

### Different path
If for some weird reason, your endpoint you want to proxy to needs you to access the default `__proxy__` route,
you can change it to something else by setting the `HIDDEN_PATH` environment variable:
```shell
HIDDEN_PATH='/__proxy__' python app.py
```

