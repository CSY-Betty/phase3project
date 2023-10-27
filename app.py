from flask import *
import boto3
import os
import mysql.connector
from dotenv import load_dotenv
import time

# load_dotenv()
load_dotenv(override=True)


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "SSSS GRIDMAN"

db_config = {
    "user": os.environ.get("rds_USER"),
    "password": os.environ.get("rds_PASSWORD"),
    "host": os.environ.get("rds_endpoint"),
    "database": os.environ.get("database_name"),
}

BUCKET_NAME = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")

Distribution_domain = os.environ.get("distribution_domain")

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET,
)


# Pages
@app.route("/", methods=["GET"])
def index():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT * FROM testdata"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    sorted_result = sorted(result, key=lambda x: x[0], reverse=True)
    messages = [(message, imageurl or "") for _, message, imageurl in sorted_result]

    # for迴圈寫法
    # messages = []
    # for id, message, imageurl in sorted_result:
    #     messages.append((message, imageurl))

    return render_template("index.html", messages=messages)


@app.route("/", methods=["POST"])
def upload_data():
    text = request.form.get("text")
    image = request.files["image"]

    current_timestamp = str(int(time.time()))
    object_name = f"{current_timestamp}_{image.filename}"

    s3.upload_fileobj(image, BUCKET_NAME, object_name)
    cloudfront_link = generate_cloudfront_link(Distribution_domain, object_name)

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    insert_query = "INSERT INTO testdata (message, imageurl) VALUES (%s, %s)"
    cursor.execute(
        insert_query,
        (
            text,
            cloudfront_link,
        ),
    )
    connection.commit()

    cursor.close()
    connection.close()

    response = jsonify({"message": "Data received successfully"})
    response.status_code = 200
    return response


def generate_cloudfront_link(distribution_domain, object_name):
    return f"https://{distribution_domain}/{object_name}"


app.run(host="0.0.0.0", port=3100)
