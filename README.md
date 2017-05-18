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
  * [Architecture](#architecture)
  * [Dependency](#dependency)

Installation
============
`git clone https://github.com/TanukiDemon/WhatDoNYC.git`

If pip for Python 3.6 is installed:
`pip install flask py2neo pandas`

Usage
=====
The application can be run locally on one's machine by executing the run.py file in the root directory like so:

`./run.py`

The browser should then be pointed to localhost:5000 with a chosen route.
These include /login, /signup, /about, /index like so:

`https://localhost:5000/about`

Architecture
============
WhatDoNYC was built using the Flask web framework. It's front end components
were written using CSS, HTML, and Javascript. Additionally, the application used
the sqlite database for user login and registration. The Neo4j graph database
was used to generate new recommendations and create a map of the relationships
between users.

Dependency
==========
  * pip
  * flask
  * pandas
  * py2neo
  * sqlalchemy
