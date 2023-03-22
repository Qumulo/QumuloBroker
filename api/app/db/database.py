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
# database.py
#
# Setup linkage to database

# Import Statements
import os

from sqlmodel import SQLModel, create_engine, Session

# db_file_name = "database.db"

DATABASE_URL = "mysql+mysqldb://"+os.environ.get('MYSQL_USER')+":"+os.environ.get('MYSQL_PASSWORD')+"@db:3306/"+os.environ.get('MYSQL_DATABASE')

# Create the DB engine
engine = create_engine(DATABASE_URL, echo=True, pool_recycle=3600)

# Create the database(s)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Create a DB session for an operation
def get_session():
    with Session(engine) as session:
        yield session
