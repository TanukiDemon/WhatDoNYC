<html>
  <link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
  <head>
    {% if title %}
    <title>{{ title }} - WhatDoNYC</title>
    {% else %}
    <title>Find your next do</title>
    {% endif %}
  </head>
  <body>
    <div>Meetup: <a href="https://meetup.com">Home</a></div>
    <hr>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
        {% for message in messages %}
            <li>{{ message }} </li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
  </body>
</html>
