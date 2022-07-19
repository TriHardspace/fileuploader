from flask import Flask, flash, request, redirect, jsonify, render_template
import boto3
from botocore.errorfactory import ClientError
import os
from werkzeug.utils import secure_filename
import random
import string

safe_urls = ['uploads.trihard.space', 'trollpepe.com', 'trolling.solutions', 'holocaust.today', 'africans.shop', 'shitpost.domains', 'stds.gay']
app = Flask(__name__)
upload_folder = './'
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000 * 1000
aws_access = os.environ["s3_access"]
aws_secret = os.environ["s3_secret"]
bucket = os.environ["s3_bucket"]
s3 = boto3.client('s3', endpoint_url="https://s3.wasabisys.com", aws_access_key_id=aws_access, aws_secret_access_key=aws_secret)
transfer = boto3.s3.transfer
config = transfer.TransferConfig(multipart_threshold=1024 * 15,
                       max_concurrency=10,
                        multipart_chunksize=1024 * 25,
                        use_threads=True)


def blacklist_file(filename):
	# checks if file is an html file to prevent xss attacks
	if 'html' in filename.rsplit('.', 1)[1].lower():
		return 1
	else:
		return 0


def namegen(ext):
	name = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=10))
	if namechecker(f"{name}.{ext}") == 1:
		namegen(ext)
	return name

def namechecker(name):
	try:
		s3.head_object(Bucket=bucket, Key=name)
		return 1
	except ClientError:
		return 0	

@app.route("/", methods=['POST'])
def upload():
	file = request.files['file']
	url = request.form['Upload Site']
	if url not in safe_urls:
		return render_template('error.html', error='Invalid upload site.')
	if 'file' not in request.files:
		# check if file part is in request
		return render_template('error.html', error='File not in request')
	if '.' not in file.filename:
		return render_template('error.html', error='Illegal file extension')
	if file.filename == '':
		# checks if file is selected
		return render_template('error.html', error='File not selected')
	if blacklist_file(file.filename) == 0:
		filext = file.filename.rsplit('.', 1)[1].lower()
		filename = namegen(filext)
		filename = f"{filename}.{filext}"
		#randomizes and temporarily saves file, will be deleted after upload to s3 bucket
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		s3.upload_file(f'./{filename}', bucket, filename, Config=config)
		os.remove(f"./{filename}")
		return render_template("success.html", filename=filename, site=url)
	if blacklist_file(file.filename) == 1:
		return render_template('error.html', error='Illegal file extension')


# Uncomment the below code if you wish to host the uploader.html file using flask 
# uncomment in staging
# @app.route("/uploader", methods=['GET', 'POST'])
# def render():
# 	return render_template('uploader.html')


@app.route("/sharex", methods=['POST'])
def sharex():
	file = request.files['file']
	url = request.form['url']
	if url not in safe_urls:
		return jsonify(error="Invalid upload site")
	if 'file' not in request.files:
		# check if file part is in request
		return jsonify(error="File not included in request")
	if file.filename == '':
		# checks if file is selected
		return jsonify(error="Filename is blank")
	if blacklist_file(file.filename) == 0:
		filext = file.filename.rsplit('.', 1)[1].lower()
		filename = namegen()
		filename = f"{filename}.{filext}"
		#randomizes and temporarily saves file, will be deleted after upload to s3 bucket
		print(filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		s3.upload_file(f'./{filename}', bucket, filename, Config=config)
		os.remove(f"./{filename}")
		return jsonify(url=f"https://{url}/{filename}")
	if blacklist_file(file.filename) == 1:
		return jsonify(error="Illegal file type")

app.run(host="127.0.0.1", port=8888)
