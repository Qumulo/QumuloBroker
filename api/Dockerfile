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
# Dockerfile to create the Qumulo VaronisIntegrator image
#

# Get the base image
FROM python:3.11-bookworm

# Who is the maintainer
MAINTAINER Berat Ulualan <bulualan@qumulo.com>

# Make sure PIP is the latest version
RUN pip install --upgrade pip==21.2.3

# Load python libraries from requirements.txt
COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt
RUN rm requirements.txt

WORKDIR /code

# Copy the code
COPY app ./app

# Copy the configuration schema
# COPY config/config.schema.json ./config/

# Make sure our paths are setup for Python and the Liraries
ENV PATH=/code/qumulo/app:/root/.local:$PATH

# Execute the command when the container is instantiated
CMD ["./app/main.py"]
# CMD ["/bin/bash"]
