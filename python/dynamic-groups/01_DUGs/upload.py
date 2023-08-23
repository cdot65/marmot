import argparse
import logging
import requests
import urllib3
from config import settings


def upload_file(file_path, server, api_key):
    """
    Uploads a file to a PAN-OS server.

    Args:
        file_path (str): The path of the file to be uploaded.
        server (str): The IP address or hostname of the PAN-OS server.
        api_key (str): The API key for the PAN-OS server.

    Returns:
        bool: True if the file was uploaded successfully, False otherwise.

    Raises:
        requests.exceptions.HTTPError: If an HTTP error occurs.
        Exception: If any other error occurs.
    """
    url = f"https://{server}/api/?type=user-id"
    payload = {"key": api_key}
    files = [("file", (file_path, open(file_path, "rb"), "text/xml"))]
    headers = {}

    try:
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
            files=files,
            verify=False,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
        return False
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        return False

    logging.info("File uploaded successfully")
    return True


def main():
    """
    Main function that parses command line arguments and calls the file upload function.
    """
    parser = argparse.ArgumentParser(description="Upload XML file to PAN-OS.")
    parser.add_argument("--file_path", help="Path to the XML file")
    parser.add_argument(
        "--server", default=settings.datacenter.base_url, help="PAN-OS server IP"
    )
    parser.add_argument("--api_key", default=settings.api_key, help="PAN-OS API Key")

    args = parser.parse_args()

    # Suppress only the single InsecureRequestWarning from urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    logging.basicConfig(level=logging.INFO)
    success = upload_file(args.file_path, args.server, args.api_key)

    if not success:
        exit(1)


if __name__ == "__main__":
    main()
