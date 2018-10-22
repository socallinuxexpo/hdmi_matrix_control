# Proof of concept of Matrix controller daemon

## install dependancies
```
pip install -r requirements.txt
```

## Run without matrix to test web interface
```
python3 cmd.py -t
```
- You can then visit web page at http://127.0.0.1:5000/
- Get json of state: /outputs
- Get single output state: /output/X
- Connect output 4 to input 4
```
curl http://127.0.0.1:5000/output/4 -d "input=4" -X PUT
```

## If you have TESmartMatrix 
```
python3 cmd.py
```
