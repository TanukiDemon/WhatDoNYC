# WhatDoNYC

Description
===========
WhatDoNYC is a Flask web application written in Python 3.6.0 that aims to create
personalized recommendations for residents and visitors of New York City. It was
created as a class project to completed over the course of one semester.

Table of contents
=================

  * [Description](#description)
  * [Table of contents](#table-of-contents)
  * [Installation](#installation)
  * [Usage](#usage)
      * [Local](#local)
      * [Remote](#remote)
  * [Architecture](#architecture)
      * [Front End](#front end)
      * [Back End](#back end)
        * [General](#general)
        * [Databases](#databases)
  * [Dependency](#dependency)

Installation
============
`git clone https://github.com/TanukiDemon/WhatDoNYC.git`

Usage
=====

Local
-----
The application can be run locally on one's machine by executing the run.py file in the root directory like so:

`./run.py`

The browser should then be pointed to localhost:5000 with a chosen route.
These include /login, /signup, /about, /index like so:

[https://localhost:5000/about](https://localhost:5000/about)

Remote
------
The application is currently hosted on AWS and can be accessed [here](https://52.33.222.241:5000/about)

Architecture
============
Front End
---------
The app's front end components were written using CSS, HTML, and Javascript.

Back End
--------

General
-------
As the application was written using the Flask framework, all back end code was
written in Python 3.6.

Databases
---------
Sqlite database for user login and registration. The Neo4j graph database
was used to generate new recommendations and create a map of the relationships
between users.

Dependency
==========
  * pip
  * flask
  * pandas
  * py2neo
  * sqlalchemy
