# Crawler cluster



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
  $sudo virtualenv -p /usr/bin/python3.6 py36_env
```
2. Install Cassandra
```shell
  
```
3. Install Kafka
```shell
  # step 1: download confluent 
  $ sudo cd /opt
  $ sudo curl -O http://packages.confluent.io/archive/5.5/confluent-5.5.0-2.12.zip
  $ unzip confluent-5.5.0-2.12.zip
  # step 2: config file  /opt/confluent-5.5.0-2.12/etc/kafka/zookeeper.properties
  dataDir=/data/zookeeper
  clientPort=2181
  maxClientCnxns=0
  # step 3: config file /opt/confluent-5.5.0-2.12/etc/kafka/server.properties
  listeners=PLAINTEXT://127.0.0.1:9092
```
### Run app
```shell
```
### Performance testing

