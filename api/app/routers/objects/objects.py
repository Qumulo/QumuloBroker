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
# objects.py
#
# API router definitions for the "/rmq/objects" endpoints

# Import python libraries

import psutil, socket
import redis
import os
import json

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from db.database import get_session, engine
from routers.objects.models import (
    Objects,
    ObjectCreate,
    ObjectRead,
    ObjectUpdate,
    ConnectivityCheck,
    Credentials,
)
from utils.qumulo_check import qumulo_check


router = APIRouter(tags=["RMQ Objects"])

# Setup Redis connection
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD')
rd = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=0)

# RMQ Object API Endpoints
# Get All RMQ Objects
@router.get(
    "/", summary="Connectivity check API call", response_model=ConnectivityCheck
)
async def root(request: Request):
    if request.headers.get("X-Real-Ip") or request.headers.get("X-Forwarded-For"):
        x_real_ip = request.headers.get("X-Real-Ip")
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        return_message = {
            "message": "Connected succesfully",
            "x_real_ip": x_real_ip,
            "x_forwarded_for": x_forwarded_for,
        }
        return return_message
    else:
        raise HTTPException(status_code=404, detail="Object not found")


# Get All RMQ Objects
@router.get(
    "/v1/rmq/objects/", summary="List all RMQ Objects", response_model=list[ObjectRead]
)
def list_objects(
    *,
    session: Session = Depends(get_session),
    qumulo_connection: int = Depends(qumulo_check)
):
    if qumulo_connection == 200:
        objects = session.exec(select(Objects)).all()
        return objects
    else:
        raise HTTPException(status_code=401, detail="Authentication failure")


@router.post(
    "/v1/rmq/objects/", summary="Create an RMQ Object", response_model=ObjectRead
)
def create_object(
    *,
    session: Session = Depends(get_session),
    qumulo_connection: int = Depends(qumulo_check),
    obj: ObjectCreate
):
    if qumulo_connection == 200:
        objects = Objects.parse_obj(
            {
                "username": obj.username,
                "password": obj.password,
                "cluster_name": obj.cluster_name,
                "certificate": obj.certificate,
                "filer_id": obj.filer_id,
                "server": obj.server,
                "port": obj.port,
                "vhost": obj.vhost,
                "exchange": obj.exchange,
            }
        )
        session.add(objects)
        session.commit()
        session.refresh(objects)
        return objects
    else:
        raise HTTPException(status_code=401, detail="Authentication failure")


@router.get(
    "/v1/rmq/objects/internal/{cluster_name}",
    summary="Get an RMQ Object",
    response_model=ObjectRead,
    deprecated=True,
)
async def get_object(
    *, session: Session = Depends(get_session), cluster_name: str, request: Request
):
    # list the networks
    networks = psutil.net_if_addrs()

    # find the container ip
    for network, addrs in networks.items():
        if network.startswith("eth0"):
            for addr in addrs:
                if "AddressFamily.AF_INET" in str(addr):
                    container_ip = addr.address

    # parse the container ip for the local host internal ip
    ip_parts = container_ip.split(".")
    ip_parts[-1] = "1"
    host_ip = ".".join(ip_parts)

    # events/Publisher.py script runs an API call retrieve the filer details for each message. The response has
    # username and password of the RabbitMQ server. Due to that reason, we ca
    #
    # In a Docker setup, X-Real-Ip and X-Forwarded-For headers can be used to identify the original IP address of a client
    # when a request is proxied through one or more intermediary servers, such as a load balancer or a reverse proxy.
    #
    # Compare the client ip with the the local host internal ip
    if (
        request.client.host == host_ip
        or request.headers.get("X-Forwarded-For") == host_ip
    ):
        cache = rd.get(cluster_name)
        if cache:
            return json.loads(cache)
        else:
            
            statement = select(Objects).where(Objects.cluster_name == cluster_name)
            results = session.exec(statement)
            cluster = results.first()
            if not cluster:
                raise HTTPException(status_code=404, detail="Object not found")
            rd.set(cluster_name, json.dumps(cluster.dict()))
            return cluster
    else:
        raise HTTPException(status_code=401, detail="Authentication failure")


@router.get(
    "/v1/rmq/objects/{cluster_name}",
    summary="Get an RMQ Object",
    response_model=ObjectRead,
)
async def get_object(
    *,
    session: Session = Depends(get_session),
    cluster_name: str,
    request: Request,
    qumulo_connection: int = Depends(qumulo_check)
):
    if qumulo_connection == 200:
        statement = select(Objects).where(Objects.cluster_name == cluster_name)
        results = session.exec(statement)
        cluster = results.first()
        if not cluster:
            raise HTTPException(status_code=404, detail="Object not found")
        return cluster
    else:
        raise HTTPException(status_code=401, detail="Authentication failure")


@router.patch(
    "/v1/rmq/objects/{cluster_name}",
    summary="Update an RMQ Object",
    response_model=ObjectRead,
)
def update_object(
    *,
    session: Session = Depends(get_session),
    qumulo_connection: int = Depends(qumulo_check),
    cluster_name: str,
    obj: ObjectUpdate
):
    if qumulo_connection == 200:
        statement = select(Objects).where(Objects.cluster_name == cluster_name)
        results = session.exec(statement)
        object1 = results.first()
        if not object1:
            raise HTTPException(status_code=404, detail="Object not found")
        object_data = obj.dict(exclude_unset=True)
        for key, value in object_data.items():
            setattr(object1, key, value)
        session.add(object1)
        session.commit()
        session.refresh(object1)
        rd.delete(cluster_name)
        return object1
    else:
        raise HTTPException(status_code=401, detail="Authentication failure")


@router.delete("/v1/rmq/objects/{cluster_name}", summary="Delete an RMQ Object")
def delete_object(
    *,
    session: Session = Depends(get_session),
    qumulo_connection: int = Depends(qumulo_check),
    cluster_name: str
):
    if qumulo_connection == 200:
        statement = select(Objects).where(Objects.cluster_name == cluster_name)
        results = session.exec(statement)
        object = results.first()
        if not object:
            raise HTTPException(status_code=404, detail="Object not found")
        session.delete(object)
        session.commit()
        return {"ok": True}
    else:
        raise HTTPException(status_code=401, detail="Authentication failure")
