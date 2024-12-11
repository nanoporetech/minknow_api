import argparse
import datetime
import sys
from getpass import getpass
from pathlib import Path
from typing import Optional, Tuple
from minknow_api.tools.compatibility_helpers import datetime_utc_now

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives.asymmetric.types import (
        CertificateIssuerPrivateKeyTypes,
        PrivateKeyTypes,
    )
    from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID
    from cryptography.hazmat.primitives import serialization
except ModuleNotFoundError as e:
    print(e, file=sys.stderr)
    print(
        "This script requires the 'cryptography' package to be installed, "
        "which is not a dependency of `minknow_api`. Run `pip install "
        "cryptography` and try again.",
        file=sys.stderr,
    )
    exit(1)


def key_to_pem(
    key: rsa.RSAPrivateKey,
    encryption: serialization.KeySerializationEncryption = serialization.NoEncryption(),
) -> bytes:
    """Convert a key into PEM format, optionally encrypting it."""
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=encryption,
    )


def cert_to_pem(cert: x509.Certificate) -> bytes:
    """Convert a certificate into PEM format."""
    return cert.public_bytes(serialization.Encoding.PEM)


def load_certificate(cert_path: Path) -> x509.Certificate:
    """Load a PEM or DER encoded certificate from disk.

    Only X509 certificates are supported.
    """
    with open(cert_path, "rb") as f:
        cert_data = f.read()
    try:
        return x509.load_pem_x509_certificate(cert_data)
    except ValueError:
        return x509.load_der_x509_certificate(cert_data)


def load_private_key(key_path: Path, key_pass_file: Optional[Path]) -> PrivateKeyTypes:
    """Load a PEM encoded private key from disk.

    Args:
        key_path: The path to the key file to load.
        key_pass_file: The path to a file containing the password required
            to decrypt `key_path`.

    If a password is required but not supplied, one will be requested.

    Note that this is just a simple wrapper around load_pem_private_key()
    from the cryptography package to handle obtaining the password. If you want
    to avoid an interactive prompt, use load_pem_private_key() directly.
    """
    if key_pass_file:
        with open(key_pass_file, "rb") as f:
            key_pass = f.read()
    else:
        key_pass = None
    with open(key_path, "rb") as f:
        key_bytes = f.read()
    try:
        return serialization.load_pem_private_key(key_bytes, password=key_pass)
    except TypeError:
        if not key_pass:
            key_pass = getpass(f"Password for {key_path}: ").rstrip().encode("utf-8")
            return serialization.load_pem_private_key(key_bytes, password=key_pass)
        else:
            raise


def generate_certificate_and_key(
    name: str,
    days_valid: int,
    issuer: Optional[x509.Name] = None,
    issuer_key: Optional[CertificateIssuerPrivateKeyTypes] = None,
) -> Tuple[x509.Certificate, rsa.RSAPrivateKey]:
    """Generate a certificate and key pair suitable for use as a client certificate with
    gRPC.

    Args:
        name: The common name to assign the certificate.
        days_valid: How many days (from today) the certificate should be valid.
        issuer: The X509 subject name of the issuing authority. If omitted,
            the generated certificate will be self-signed.
        issuer_key: The private key for `issuer`. Must be provided if `issuer`
            is provided.

    The resulting certificate will only be permitted to sign other certificates
    if it is self-signed (ie: `issuer` is omitted/None).
    """
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COMMON_NAME, name),
        ]
    )

    if issuer is None:
        if issuer_key is not None:
            raise TypeError("issuer_key arg provided but issuer is None")
        issuer = subject
        issuer_key = key
        can_sign = True
    else:
        if issuer_key is None:
            raise TypeError("issuer arg provided but issuer_key is None")
        # if we've been provided with a CA, don't let this cert sign other certs
        can_sign = False

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime_utc_now())
        .not_valid_after(datetime_utc_now() + datetime.timedelta(days=days_valid))
        .add_extension(
            x509.BasicConstraints(ca=can_sign, path_length=None),
            critical=True,
        )
        .add_extension(
            # for gRPC client usage, IF the "key usage" extension is included
            # THEN "digital signature" must be set
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=can_sign,
                crl_sign=can_sign,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            # for gRPC client usage, IF the "extended key usage" extension
            # is included THEN "client auth" must be set (unsurprisingly)
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CLIENT_AUTH]),
            critical=True,
        )
        .sign(issuer_key, hashes.SHA256())
    )

    return cert, key


def main():
    parser = argparse.ArgumentParser(
        description="""Generate client certificates for MinKNOW.""",
        epilog="""This will generate a private key and a certificate chain for use as
        a client TLS certificate in gRPC. If --ca-cert is used, that CA
        certificate should be placed in conf/rpc-client-certs/ in the MinKNOW
        installation, otherwise the <name>_cert.pem file generated by this
        script should be placed in that directory.""",
    )
    parser.add_argument(
        "name",
        help="The base name of the files to output (<name>_cert.pem, <name>_key.pem)",
    )
    parser.add_argument(
        "--common-name",
        help="The identity (common name) of the certificate - <name> will be used by default",
    )
    key_pass_group = parser.add_mutually_exclusive_group()
    key_pass_group.add_argument(
        "--key-pass-file",
        type=Path,
        help="File containing a passphrase to encrypt the private key with",
    )
    key_pass_group.add_argument(
        "--no-key-pass", action="store_true", help="Store the private key unencrypted"
    )
    parser.add_argument(
        "--days-valid",
        default=365,
        type=int,
        help="The number of days the certificate will be valid for",
    )
    parser.add_argument(
        "--ca-cert",
        type=Path,
        help="Sign the certificate using the given CA certificate",
    )
    parser.add_argument(
        "--ca-key", type=Path, help="Key for the certificate given by --ca-cert"
    )
    parser.add_argument(
        "--ca-key-pass-file",
        type=Path,
        help="File containing the passphrase for the key given by --ca-key",
    )
    args = parser.parse_args()

    if args.ca_cert and not args.ca_key:
        parser.error("If --ca-cert is provided, --ca-key must also be provided")

    if args.common_name:
        name = args.common_name
    else:
        name = Path(args.name).stem

    if args.no_key_pass:
        key_encryption = serialization.NoEncryption()
    elif args.key_pass_file:
        with open(args.key_pass_file, "rb") as f:
            key_encryption = serialization.BestAvailableEncryption(f.read())
    else:
        # prompt
        while True:
            key_pass = getpass(
                "Choose a private key password (enter for no password): "
            )
            if not key_pass:
                break
            key_pass_check = getpass("Confirm password: ")
            if key_pass == key_pass_check:
                break
            print("Passwords do not match", file=sys.stderr)
        if key_pass:
            key_encryption = serialization.BestAvailableEncryption(
                key_pass.encode("utf-8")
            )
        else:
            key_encryption = serialization.NoEncryption()

    if args.ca_cert:
        ca_cert = load_certificate(args.ca_cert)
        cert, key = generate_certificate_and_key(
            name,
            days_valid=args.days_valid,
            issuer=ca_cert.subject,
            issuer_key=load_private_key(args.ca_key, args.ca_key_pass_file),
        )
    else:
        cert, key = generate_certificate_and_key(name, days_valid=args.days_valid)
        ca_cert = None

    # Write our certificate out to disk.

    with open(f"{args.name}_key.pem", "wb") as f:
        f.write(key_to_pem(key, key_encryption))

    with open(f"{args.name}_cert.pem", "wb") as f:
        f.write(cert_to_pem(cert))
        # make this a certificate chain, because that's what gRPC will want:
        if ca_cert:
            f.write(cert_to_pem(ca_cert))


if __name__ == "__main__":
    main()
