# Proof of concept of Matrix controller daemon

## Install dependencies
```bash
python3 -m venv venv
. venv/bin/activate
pip3 install .
```

## Run without matrix to test web interface
```bash
hdmi-mx -t
```
- You can then visit web page at http://127.0.0.1:5000/
- Get json of state: /outputs
- Get single output state: /output/X
- Connect output 4 to input 4
```
curl http://127.0.0.1:5000/output/4 -d "input=4" -X PUT
```

## If you have TESmartMatrix 
```bash
hdmi-mx
```

## Setup Dev Environment with New Pipenv
The new tool endorsed by the PyPA is Pipenv. It manages dependencies and virtual environments, providing a "bundler" or "npm" like experience.
```bash
pipenv install --dev --pre
pipenv run hdmi-mx
```
