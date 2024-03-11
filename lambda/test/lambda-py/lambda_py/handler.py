import boto3
import qrcode
import io

sts = boto3.client("sts")


def text_qr(data):
    qr = qrcode.QRCode()
    qr.add_data(data)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    return f.read()


def handle(event, context):
    response = sts.get_caller_identity()
    account = response.get("Account", "???")
    return text_qr(account)


if __name__ == "__main__":
    print(handle(None, None))
