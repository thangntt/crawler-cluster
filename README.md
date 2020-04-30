# Crawler cluster

## Overview
Crawler Cluster is a web crawling system, allowing to build crawlers of any scale and purpose. It includes:
* [Scrapy](https://github.com/scrapy/scrapy) is a fast high-level web crawling and web scraping framework, used to crawl websites and extract structured data from their page. It can be used for a wide range of purposes, from data mining to monitoring and automated testing.

## Setup and Run 
### Requirements:
1. Python 3
2. Ubuntu
3. Cassandra
4. Kafka

### Install environment (on Ubuntu)
1. Install Python3
```shell
  # step 1: install python3.6 with command
  $sudo apt-get install python3.6
  # step 2: instal pip3 with command
  $sudo apt-get install python3-pip
  # step 3: install virtualenv with command
  $sudo pip3 install virtualenv
  # step 4: create a vitualt environment 
  $sudo virtualenv -p /usr/bin/python3.6 /opt/py36_env
```
2. Install Cassandra
```shell
  # step 1: download cassandra 
  $sudo cd /opt
  $sudo wget http://mirrors.viethosting.com/apache/cassandra/3.0.20/apache-cassandra-3.0.20-bin.tar.gz
  $tar -xzvf apache-cassandra-3.0.20-bin.tar.gz
  # step 2: creat folder
  $sudo mkdir -p /data/cassandra/commitlog
  $sudo mkdir -p /data/cassandra/data
  $sudo mkdir -p /data/cassandra/saved_cahes
  # step 2: config file conf/cassandra.yaml 
  seed_provider:
  - class_name: org.apache.cassandra.locator.SimpleSeedProvider
    parameters:
         - seeds: "127.0.0.1"
  listen_address: 127.0.0.1
  endpoint_snitch: SimpleSnitch
  data_file_directories:
      - /data/cassandra/data
  commitlog_directory: /data1/cassandra/commitlog
  saved_caches_directory: /data1/cassandra/saved_caches
  rpc_address:  0.0.0.0
  authenticator: PasswordAuthenticator
  broadcast_rpc_address: 127.0.0.1
```
3. Install Kafka
```shell
  # step 1: download confluent 
  $sudo cd /opt
  $sudo wget http://packages.confluent.io/archive/5.5/confluent-5.5.0-2.12.zip
  $unzip confluent-5.5.0-2.12.zip
  # step 2: config file etc/kafka/zookeeper.properties
  dataDir=/data/zookeeper
  clientPort=2181
  maxClientCnxns=0
  # step 3: config file /etc/kafka/server.properties
  listeners=PLAINTEXT://127.0.0.1:9092
```
### Run app
```shell
  # step 1: run kafka
  $sudo cd /opt/confluent-5.5.0-2.12
  $sudo ./bin/zookeeper-server-start etc/kafka/zookeeper.properties
  $sudo ./bin/kafka-server-start etc/kafka/server.properties
  # step 2: run cassandra
  $sudo cd /opt/apache-cassandra/bin
  $sudo ./cassandra
  # test login cassandra
  $sudo./cqlsh -u cassandra -p cassandra
  # step 3: clonse app and install lib 
  $sudo cd /opt
  $sudo git clonse https://github.com/thangntt/crawler-cluster.git
  $/opt/py36_env/bin/pip3 install -r /opt/crawler-cluster/requirements.xtx 
  # step 4: run app
  $cd /opt/crawler-cluster/
  $sudo /opt/py36_env/bin/python3.6 sample/setup.py
  $sudo /opt/py36_env/bin/python3.6 crawler/schedule.py
  $sudo /opt/py36_env/bin/python3.6 sample/crawl_data.py
```
### Performance testing

