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
# models.py
#
# Definitions of the models

from typing import Optional

from sqlmodel import Field, SQLModel

class ObjectBase(SQLModel):
    cluster_name: str 
    certificate: str
    filer_id: int = Field(index=True, unique=True)
    server: str
    port: int
    vhost: str
    exchange: str
    username: str
    password: str

class Objects(ObjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
# Create a Object entry in the DB
class ObjectCreate(ObjectBase):
    pass

# Read from the Objects table
class ObjectRead(SQLModel):
    id: int
    cluster_name: str
    certificate: str
    filer_id: int
    server: str
    port: int
    vhost: str
    exchange: str
    username: str
    password: str

# Update a Object entry in the DB
class ObjectUpdate(SQLModel):
    cluster_name: Optional[str]
    certificate: Optional[str]
    filer_id: Optional[int]
    server: Optional[str]
    port: Optional[int]
    vhost: Optional[str]
    exchange: Optional[str]
    username: Optional[str]
    password: Optional[str]
    
class Credentials(SQLModel):
    username: str
    password: str
    cluster: str
    
class ConnectivityCheck(SQLModel):
    message: str
    x_real_ip: str
    x_forwarded_for: str
    