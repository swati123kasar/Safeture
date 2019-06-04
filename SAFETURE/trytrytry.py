from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World'


$data='{"medicine":"cipla","medicine_id":"sanglipunecipla","quality":"Good","timestamp":"Wed Oct  3 07:23:13 2018"}';

<a href="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=<?php echo urlencode($data);?>">Get Your Code</a>


if __name__ == '__main__':
   app.run()