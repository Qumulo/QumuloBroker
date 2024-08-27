import requests
import json
import argparse
import sys

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Field, SQLModel


class Credentials(SQLModel):
    username: str
    password: str
    cluster: str


from utils.logger import Logger

# python + ssl on MacOSX is rather noisy against dev clusters
requests.packages.urllib3.disable_warnings()

# Define the name of the Program, Description, and Version.
progname = "Qumulo RestAPIs for Varonis"
progdesc = "Qumulo RestAPIs for Varonis"
progvers = "7.2.0"

# Start by getting any command line arguments

parser = argparse.ArgumentParser(description=progdesc)
parser.add_argument(
    "--version", action="version", version=f"{progname} - Version {progvers}"
)
parser.add_argument(
    "--log",
    default="INFO",
    required=False,
    dest="loglevel",
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "DEBUG"],
    help="Set the logging level.",
)
parser.add_argument(
    "--cluster", dest="cluster", default="", help="The cluster address."
)
parser.add_argument(
    "--username", dest="username", default="", help="The cluster username."
)
parser.add_argument(
    "--password", dest="password", default="", help="The cluster password."
)
try:
    args = parser.parse_args()
except argparse.ArgumentTypeError:
    # Log an error
    sys.exit(1)

# Build a logger to handle logging events.
logger = Logger(name=progname, version=progvers, level=args.loglevel, log_path=None)


async def qumulo_check(credentials: Credentials, request: Request):
    print(request.client.host)
    root_url = f"https://{credentials.cluster}:8000"

    who_am_i_url = root_url + "/v1/session/who-am-i"
    cluster_info_url = root_url + "/v1/cluster/settings"
    login_url = root_url + "/v1/session/login"

    default_header = {"content-type": "application/json"}
    post_data = {"username": credentials.username, "password": credentials.password}

    try:
        resp = requests.post(
            login_url,
            data=json.dumps(post_data),
            headers=default_header,
            verify=False,
            timeout=5,
        )

        resp.raise_for_status()

        if resp.status_code == 200:
            bearer_token = json.loads(resp.text)["bearer_token"]
            default_header["Authorization"] = f"Bearer {bearer_token}"

            try:
                resp = requests.get(
                    cluster_info_url, headers=default_header, verify=False, timeout=5
                )

                logger.info(resp.status_code)

            except requests.ConnectionError as e:
                # retry the request or raise an error
                logger.error(f"{e}")
            except requests.HTTPError as e:
                # check the status code and handle the error
                if resp.status_code == 404:
                    # resource not found
                    logger.error(f"{e}")
                elif resp.status_code == 401:
                    # unauthorized
                    logger.error(f"{e}")
            except requests.exceptions.InvalidURL as e:
                logger.error(f"{e}")
            except requests.exceptions.Timeout as e:
                logger.error(f"{e}")
            except KeyboardInterrupt as e:
                logger.error(f"{e}")

    except requests.HTTPError as e:
        # check the status code and handle the error
        if resp.status_code == 404:
            # resource not found
            logger.error(f"{e}")
        elif resp.status_code == 401:
            # unauthorized
            logger.error(f"{e}")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"{e}")
    except requests.exceptions.InvalidURL as e:
        logger.error(f"{e}")
    except requests.exceptions.Timeout as e:
        logger.error(f"{e}")
    except KeyboardInterrupt as e:
        logger.error(f"Operation was cancelled by the user manually.")

    print(resp.status_code)
    return resp.status_code


# def main():
#     # qumulo_check({"cluster" : args.cluster, "username" : args.username, "password" : args.password})
#     qumulo_check(json.dumps({"cluster" : args.cluster, "username" : args.username, "password" : args.password}))

# if __name__ == "__main__":
#     main()
