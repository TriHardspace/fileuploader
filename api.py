from flask import Flask, flash, request, redirect, render_template
import boto3
import os
from werkzeug.utils import secure_filename
import random
import string

app = Flask(__name__)
upload_folder = './'
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000 * 1000
aws_access = os.environ["s3_access"]
aws_secret = os.environ["s3_secret"]
bucket = os.environ["s3_bucket"]
s3 = boto3.client('s3', endpoint_url="https://s3.wasabisys.com", aws_access_key_id=aws_access, aws_secret_access_key=aws_secret)

def blacklist_file(filename):
	# checks if file is an html file to prevent xss attacks
	if 'html' in filename.rsplit('.', 1)[1].lower():
		return 1
	else:
		return 0


def namegen():
	file = open('/dev/urandom', 'rb')
	name = ""
	for i in range(8):
		name=name+str(file.read(i))
	name = bytes(name, 'utf-8')
	name = int.from_bytes(name, 'big')
	name = str(name)
	name = name[:10]
	return(name)


@app.route("/", methods=['POST'])
def upload():
	file = request.files['file']
	if 'file' not in request.files:
		# check if file part is in request
		flash('No file part')
		return redirect(request.url)
	if file.filename == '':
		# checks if file is selected
		flash('No file selected')
		return redirect(request.url)
	if blacklist_file(file.filename) == 0:
		filext = file.filename.rsplit('.', 1)[1].lower()
		filename = namegen()
		filename = f"{filename}.{filext}"
		#randomizes and temporarily saves file, will be deleted after upload to s3 bucket
		print(filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		s3.put_object(Body=f"./{filename}", Bucket=bucket, Key=filename)
		os.remove(f"./{filename}")
		return render_template("success.html", filename=filename)


app.run(host="0.0.0.0", port=8888)
