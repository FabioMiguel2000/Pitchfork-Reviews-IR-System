#!/bin/bash

cd ../system_1/
docker build . -t system_1
docker run --name system_1 -p 8981:8983 -d system_1

cd ../system_2/
docker build . -t system_2
docker run --name system_2 -p 8982:8983 -d system_2

cd ../system_3/
docker build . -t system_3
docker run --name system_3 -p 8983:8983 -d system_3

cd ../system_4/
docker build . -t system_4
docker run --name system_4 -p 8984:8983 -d system_4

cd ../system_5/
docker build . -t system_5
docker run --name system_5 -p 8985:8983 -d system_5

cd ../system_6/
docker build . -t system_6
docker run --name system_6 -p 8986:8983 -d system_6