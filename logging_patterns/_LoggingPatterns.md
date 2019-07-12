theme: Simple, 1
footer: ![3%](elastic-footer.png)　　<sup>@emanuil_tolev</sup>



![](pattern.jpg)

# **Centralised**
# [fit] Logging Patterns
## <br><br><br>Emanuil Tolev　　　　　@emanuil_tolev
## <br><br><br>Based heavily on lots of work by<br>Philipp Krenn, @xeraa

---

![fit](console.png)

---

![fit](cat.png)

^ Who is doing that.

---

![fit](tail.png)

^ Or maybe even this?

---

![fit](less.png)

^ What is the advantage of less +F over tail -f?
Follows but you can [ctrl]+[c] any time and search (/foobar), scroll, jump to the end (G),...

---

![150%](this-is-fine.png)

---

![fit](lesser.png)

---

![fit](lessest.png)

---

![120%](this-is-not-fine.jpg)

---

[.hide-footer]
![fit](all.jpg)

---

# ![80%](elastic.png)
# Community Engineer

---

<!--
# Questions: [http://sli.do/xeraa](http://sli.do/xeraa)
## Answers: [https://xeraa.net](https://xeraa.net)

---
-->

<!--
# ![150%](elasticsearch.png)

^ Compass 1 + 2
  2010 Shay Banon

---

![45%](github.png)
![125%](stackoverflow.png)
![25%](wikipedia.png)

---

![left 110%](kibana.png)
![right 100%](logstash.png)

---
-->

![60%](elk.png)

---

![original 70%](lyft.png)
![original 28%](slack.png)
![original 95%](fitbit.png)

---

![40%](elkb.png)

---

![60%](belk.png)

---

![45%](stack.png)

---

[.hide-footer]
# ![67%](elastic-stack.png)

---

# Licensing
## **Open Source** Apache-2.0
## **Basic** free
## **Commercial** 💸

---

## Disclaimer
# We're going to look at nothing more than **highly** monitored Hello World app

---

# Example: Java
## SLF4J, Logback, MDC

---

# And Everywhere Else
## .NET: NLog
## PHP: Monolog
## JavaScript: Winston
## Python: structlog

---
<!--
# Anti-Pattern: `print`
## `System.out.println("Oops");`

^ Before getting started, let's clear up two anti-patterns we want to avoid

---

# Anti-Pattern: Coupling

---

[.hide-footer]
![50%](6-5.png)

^ This was released tonight, so obviously I updated my demo today

---
-->

[.hide-footer]
![autoplay](hold-on.mp4)

---

# [fit] 　　Parse 🔪　　

^ Who's doing this? Who likes writing regex?

---

![100%](parse.png)

---

```
[2018-09-28 10:30:38.516] ERROR net.xeraa.logging.LogMe [main] -
                          user_experience=🤬, session=46, loop=15 -
                          Wake me up at night
java.lang.RuntimeException: Bad runtime...
  at net.xeraa.logging.LogMe.main(LogMe.java:30)


^\[%{TIMESTAMP_ISO8601:timestamp}\]%{SPACE}%{LOGLEVEL:level}
  %{SPACE}%{USERNAME:logger}%{SPACE}\[%{WORD:thread}\]
  %{SPACE}-%{SPACE}%{GREEDYDATA:mdc}%{SPACE}-%{SPACE}
  %{GREEDYDATA:themessage}(?:\n+(?<stacktrace>(?:.|\r|\n)+))?
```

---
<!--
[.hide-footer]
![fit](multiline.png)

---

![right 68%](ecs.png)

# Elastic Common Schema
## [https://github.com/elastic/ecs](https://github.com/elastic/ecs)

---
-->

![right fit](grok.png)

## Dev Tools
# Grok Debugger

---

![right fit](visualizer.png)

## Machine Learning
# Data Visualizer

---

# Log and Infrastructure UI

^ Logs, live streaming, Infrastructure tab. We get the info in Infra from metricbeat.

---
<!--
![right 47%](monitoring.png)

# Monitoring: Logstash Pipeline
## Plus other components

---
-->
# Pro: No change
# Con: RegEx, timestamp, multiline

^ timestamp - timezones are hard

---

# [fit] 　　Send ✉️　　

^ Who's doing this?

---

![100%](send.png)

^ Async in its own thread

---

# Pro: No files
# Con: Outages & coupling

^ Backlog queue default 200MB
Dying container might not send all the logs
Very early startup errors might not even reach the log appender
Changes in the Logstash config need to be redeployed everywhere

---

# [fit] 　　Structure 🕸　　

---

![100%](structure.png)

^ logback.xml 33-37 this is how to integrate an appender. The config is it sends to logstash.

---

# Pro: Right format
# Con: JSON serialization overhead

---

# [fit] 　　Containerize 📦　　

---

![20%](docker.png)

^ Anybody using something else than Docker? No? Yeah, I didn't think so

---

## Where to put Filebeat?
# Sidecar

^ could put on the docker host itself too

---

## [https://github.com/elastic/beats/tree/master/deploy/docker](https://github.com/elastic/beats/tree/master/deploy/docker)
---
# Docker Logs
```yml
filebeat.autodiscover:
  providers:
    - type: docker
      hints.enabled: true
```
---
# Hints
```yml
labels:
  - "app=fizzbuzz"
  - "co.elastic.logs/multiline.pattern=^\\["
  - "co.elastic.logs/multiline.negate=true"
  - "co.elastic.logs/multiline.match=after"
```

^ An inversion of where we configure logging. Here we say what the logging will look like where the app container is defined rather than hardcode it into the logging filebeat container. Prev. slide has hints.enabled: true to tie this together.

---
# Metadata
## No metadata with other methods
```js
{
  "docker": {
    "container": {
      "image": "python-logging_python_app",
      "labels": {
        "com": {
          "docker": {
            "compose": {
              "container-number": "1",
              "project": "python-logging",
              "service": "python_app",
              "version": "1.23.2",
              "oneoff": "False",
              "config-hash": "2b38df3c73c6   1a68a37443c2006f3f3e4fc16c3c   2a1d7793f2a38841e274b607"
            }
          }
        },
        "app": "fizzbuzz"
      },
      "id": "9d6d5a7640a457a1e08c422cb0a08   f96ff3631fb5356f749b2ac7d8f3719687f"   ,
      "name": "python_app"
    }
  }
}
```
---
# Registry File
```yml
filebeat.registry_file: /usr/share/filebeat/data/registry
```

^ Keep external on a volume if you replace the Filebeat container and don't want to recollect all the logs

---

# Configuration Templates

```
                _._
           _.-``__ ''-._
      _.-``    `.  `_.  ''-._           Redis 4.0.9 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._
 (    '      ,       .-`  | `,    )     Running in stand alone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 55757
  `-._    `-._  `-./  _.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |           http://redis.io
  `-._    `-._`-.__.-'_.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |
  `-._    `-._`-.__.-'_.-'    _.-'
      `-._    `-.__.-'    _.-'
          `-._        _.-'
              `-.__.-'
```

^ Sometimes you need very specific parsing rules to get rid of some logging crap

---
# Configuration Templates
```yml
filebeat.autodiscover:
  providers:
    - type: docker
      templates:
        - condition:
            equals:
              docker.container.image: redis
          config:
            - type: docker
              containers.ids:
                - "${data.docker.container.id}"
              exclude_lines: ["^\\s+[\\-`('.|_]"]  # Drop asciiart lines
```

---

![75%](kubernetes.png)

---

## Where to put Filebeat?
# DaemonSet
^ Ensures that all nodes run a copy of a pod

---

## [https://github.com/elastic/beats/tree/master/deploy/kubernetes](https://github.com/elastic/beats/tree/master/deploy/kubernetes)

---

# Metadata
## Either in cluster or not
```yml
processors:
- add_kubernetes_metadata:
    in_cluster: true
- add_kubernetes_metadata:
    in_cluster: false
    host: <hostname>
    kube_config: ${HOME}/.kube/config
```

^ Second example enables the processor on a Beat running as a process on the Kubernetes node

---

# Metadata
```json
{
  "host": "172.17.0.21",
  "port": 9090,
  "kubernetes": {
    "container": {
      "id": "382184ecdb385cfd5d1f1a65f78911054c8511ae009635300ac28b4fc357ce51",
      "image": "my-python:1.0.0",
      "name": "my-python"
    },
    "labels": {
      "app": "python",
    },
    "namespace": "default",
    "node": {
      "name": "minikube"
    },
    "pod": {
      "name": "python-2657348378-k1pnh"
    }
  },
}
```

^ When filebeat is run as a pod in Kubernetes

---

# Configuration Templates
```yml
filebeat.autodiscover:
  providers:
    - type: kubernetes
      templates:
        - condition:
            equals:
              kubernetes.namespace: redis
          config:
            - type: docker
              containers.ids:
                - "${data.kubernetes.container.id}"
              exclude_lines: ["^\\s+[\\-`('.|_]"]  # Drop asciiart lines
```

---

# Customize Indices
```yml
output.elasticsearch:
  index: "%{[kubernetes.namespace]:filebeat}-%{[beat.version]}-%{+yyyy.MM.dd}"
```

^ beat.version in case you upgrade in the middle of the day and there's a mapping conflict

---

# [fit] 　　Wrapup Logging　　

---

# Examples
## [https://github.com/xeraa/java-logging](https://github.com/xeraa/java-logging)

---

## Parse 🔪
## Send ✉️
## Structure 🕸
## Containerize 📦
## Orchestrate 🎻

^ Parse - send log file to logstash, parse in a central place, but too much regex.
^ Send - send info directly to central place from the app without a Beat/shipper, but network may be down.
^ Structure - produce log in the right format, ship it without parsing. Avoids dehydrating the meaning of the logs from app to file, rehydrating to log infrastructure. Good option if you don't have containers.
^ Containerize: often you'll start containerising old apps that just write logs, so we went over what to do there. You could use direct structured JSON with docker too.
^ Orchestrate: same as containerize but with Kubernetes awareness and deployment specifics.

---

# [fit] 　　Questions?
### <br><br><br>Emanuil Tolev　　　　　@emanuil_tolev
### <br><br><br>Philipp Krenn　　　　　@xeraa
