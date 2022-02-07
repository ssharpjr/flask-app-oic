# Dockerfile for building the Oracle Instant Client on Ubuntu 18.04
FROM ubuntu:18.04

# Set the working directory to /app
WORKDIR /app

# Place the Oracle Instant Client RPM files in the same directory as this Dockerfile
COPY . /app

# Install packages (and clean them up)  iproute2, iputils-ping for dev
RUN apt-get update
RUN apt-get install -y iproute2 alien libaio1 \
        python3 python3-pip && \
	alien -i /app/oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm && \
	alien -i /app/oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm && \
	alien -i /app/oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64.rpm && \
	rm -rf /app/oracle-instantclient* && \
	apt-get purge alien -y && apt-get autoremove -y && apt-get autoclean && \
	mkdir -p /usr/lib/oracle/12.2/client64/network

# Copy Oracle config files
COPY tnsnames.ora /usr/lib/oracle/12.2/client64/network

# Set ENV Variables
ENV ORACLE_HOME=/usr/lib/oracle/12.2/client64
ENV TNS_ADMIN=$ORACLE_HOME/network
ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib
ENV PATH=$PATH:$ORACLE_HOME/bin

# Install app requirements separately for testing
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python3", "app.py"]
