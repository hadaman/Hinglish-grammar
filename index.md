---
layout: default
title: Home
---

# Welcome

This blog auto-imports posts from an RSS feed. New posts will appear below.

<ul>
{% for post in site.posts %}
  <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> — <small>{{ post.date | date: "%b %-d, %Y" }}</small></li>
{% endfor %}
</ul>
