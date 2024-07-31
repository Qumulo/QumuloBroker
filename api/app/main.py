#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Qumulo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------
# main.py
#
# API Definitions for Varonis RabbitMQ operations. This routine defines
# all of the API endpoints and database connections for that API. Also, it will manage
# the startup of all of the other containers; thus removing the need for complicated
# docker-compose files.

# Import python libraries
import argparse
import sys
import uvicorn
from fastapi import FastAPI

# Import required python files and function from other files
from utils.logger import Logger
from db.database import engine
from db.database import create_db_and_tables
from routers.objects import objects

import time
time.sleep(10)

# Define the name of the Program, Description, and Version.
progname = "Qumulo RestAPIs for Varonis"
progdesc = "Qumulo RestAPIs for Varonis"
progvers = "5.3.2"

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
try:
    args = parser.parse_args()
except argparse.ArgumentTypeError:
    # Log an error
    sys.exit(1)

# Build a logger to handle logging events.
logger = Logger(name=progname, version=progvers, level=args.loglevel, log_path=None)

# Instantiate the API
app = FastAPI(
    title=progname,
    description=progdesc,
    version=progvers,
    terms_of_service="https://www.qumulo.com/terms-hub",
    contact={
        "name": "Qumulo Care",
        "url": "https://care.qumulo.com",
        "email": "care@qumulo.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://choosealicense.com/licenses/mit/",
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# Include all of the endpoints
app.include_router(objects.router)


# Functions to execute on startup before we deal with the API
@app.on_event("startup")
async def startup_event():
    logger.info("Startup event reached")
    create_db_and_tables()


# Functions that will help us terminate
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutdown event reached")


# Main routine that starts up everything!!
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False, proxy_headers=True)


if __name__ == "__main__":
    main()
