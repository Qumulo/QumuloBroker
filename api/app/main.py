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
import time
import uvicorn
from fastapi import FastAPI

# Import required modules from other files
from utils.logger import Logger
from db.database import create_db_and_tables
from routers.objects import objects

progname = "Qumulo RestAPIs for Varonis"
progdesc = "Qumulo RestAPIs for Varonis"
progvers = "7.2.0"

def parse_args():
    """Parse command-line arguments."""
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
    return parser.parse_args()

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    # Define the lifespan event
    async def lifespan(app: FastAPI):
        logger.info("Starting up application...")
        create_db_and_tables()
        yield
        logger.info("Shutting down application...")

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
        lifespan=lifespan
    )

    # Include all of the endpoints
    app.include_router(objects.router)

    return app

def main():
    args = parse_args()

    global logger
    logger = Logger(name=progname, version=progvers, level=args.loglevel, log_path=None)

    logger.info("Sleeping for 10 seconds before starting the application...")
    time.sleep(10)

    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False, proxy_headers=True)

if __name__ == "__main__":
    main()
