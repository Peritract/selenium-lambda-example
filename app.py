from os import environ as env
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from dotenv import load_dotenv
from xhtml2pdf import pisa
import plotly_express as px
import boto3


def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return True on success and False on errors
    return pisa_status.err

def create_report():
    img_bytes = px.scatter([1, 2, 3], [4, 5, 6]).to_image()
    img = base64.b64encode(img_bytes).decode("utf-8")
    template = f'''
    <h1>TMNT</h1>
    <p>Example!</p>
    <img style="width: 400; height: 600" src="data:image/png;base64,{img}">
    '''

    convert_html_to_pdf(template, env.get("REPORT_FILE"))


def send_email():

    client = boto3.client("ses",
                          region_name="eu-west-2",
                          aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
                          aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"])
    message = MIMEMultipart()
    message["Subject"] = "Local Test"

    attachment = MIMEApplication(open(env.get("REPORT_FILE"), 'rb').read())
    attachment.add_header('Content-Disposition', 'attachment', filename='report.pdf')
    message.attach(attachment)

    print(message)

    client.send_raw_email(
        Source='dan.keefe@sigmalabs.co.uk',
        Destinations=[
            'dan.keefe@sigmalabs.co.uk',
        ],
        RawMessage={
            'Data': message.as_string()
        }
    )



def handler(event, context):
    create_report()
    print("Report created.")
    send_email()
    print("Email sent.")


if __name__ == "__main__":
    load_dotenv()
    print(handler(None, None))
