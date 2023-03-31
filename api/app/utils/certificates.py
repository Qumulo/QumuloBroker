import base64
import requests
import json
import argparse
import sys

from sqlmodel import Field, SQLModel


class EncodeCertificate(SQLModel):
    file_path: str


class DecodeCertificate(SQLModel):
    certificate: str


def encode_certificate(certificate: EncodeCertificate):
    # read the .crt file
    with open(certificate.file_path, "rb") as f:
        cert_data = f.read()
    # encode the file data as a base64 string
    encoded_cert = base64.b64encode(cert_data).decode()

    return encoded_cert


def decode_certificate(certificate: DecodeCertificate):
    # read the .crt file
    with open(certificate.file_path, "rb") as f:
        cert_data = f.read()
    # encode the file data as a base64 string
    decoded_cert = base64.b64decode(cert_data).decode()

    return decoded_cert
