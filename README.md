# MASTER-WORKERs-SCRAPER
<p>
  <a href="https://circleci.com/gh/vuejs/vue/tree/dev"><img src="https://img.shields.io/circleci/project/github/vuejs/vue/dev.svg?sanitize=true" alt="Build Status"></a>
  <a href="https://www.npmjs.com/package/vue"><img src="https://img.shields.io/npm/l/vue.svg?sanitize=true" alt="License"></a>
</p>

---

## Info
> This is a starter project for master-workers scraper within the docker. The master-scraper will auto-update the new post on (ex: twitter) and check if there is an update from single user, master will create a worker to helping out scraping the detail data and store it to mySQL
## Tech

## Environment
* **HOST**: unix system
* **Docker**: version 20.10.5
* **Docker-compose**: version 1.28.5
* **Docker-py**: version: 4.4.4
* other python library requirements has already been stated in requirements.txt
## Structure
* **Master** (python:3.8) - updating new data and manipulate the lifecycle of workers
* **Workers** (python:3.8) - connecting to openVPN and start scraping detail data from specific account assigned by master
* **Host** (unix) - with the docker daemon and connect to master docker SDK by binding UNIX socket
* **backend-network**: network connecting between master and workers
* **Database** (mySQL:8) - using host:3000 <-> master:3306, storing the data scraped from the workers
* **Redis** - using redis as the alternative wat to create an channel between master(publisher) <-> workers(subscriber)

## Before Starting
1. Create your own `.env` and fill out them if you needed
2. Since there is an openvpn stuff in worker `Dockerfile`, I'm using the Surfshark for the credential.
3. There is a production mode which using GCP cloud SQL proxy~ You should set up your own cloud sql proxy first to connect and paste the credential inside `/credentials/clousSql.json` 
## Initialize
Using docker is easy!
```shell
docker-compose build
docker-compose up
```