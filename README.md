# TEA (TLS Exception Analyzer)
[![Repo on GitHub](https://img.shields.io/badge/repo-GitHub-222222.svg?style=flat&logo=github)](https://github.com/irworks/tea)
[![Repo on GitLab](https://img.shields.io/badge/repo-GitLab-fc6d26.svg?style=flat&logo=gitlab)](https://git.mp-software.io/RUB-AI/bachelor-arbeit/tls-analyzer)
[![license](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE.md)
[![Python Version](https://img.shields.io/badge/python-3.7%20|%203.9-blue)](https://git.mp-software.io/RUB-AI/bachelor-arbeit/tls-analyzer)

Analyze iOS apps regarding [App Transport Security (ATS)](https://developer.apple.com/documentation/security/preventing_insecure_network_connections) exception and extract urls and domains.   

![TEA Dashboard](/screenshots/dashboard.png?raw=true "TEA Dashboard")

### Usage
Prepare a folder containing `.ipa` files for analysis. To extract multiple apps at once you can use [ipdumper](https://gitlab.com/marzzzello/ipa-dumper).

### Parameters
Full example: `python -m flask analyze -w /home/testdir -v INFO -c true`
#### Required
- `--work-dir` (`-w`)
  - Specify your working directory.

#### Optional
- `--verbosity` (`-v`) 
  - Log level, values: [`INFO, WARNING, DEBUG`]
  - **Default:** `INFO`
- `--cleanup` (`-c`) 
  - Extract in place: When `true`, the extracted `.ipa` directories are deleted in order to save space. Original `.ipa` files are always untouched.
  - **Default:** `false`

### Output
Currently, the data is stored in a SQLite database as can be seen in `config.py` and controlled via `.flaskenv`

## Deployment
To deploy the web-application a `Dockerfile` is provided.

### Docker
To build a Docker image run inside the directory including the Dockerfile
the following command.
```shell
  $ docker build --tag tea .
```

To start a new container with the name _tea-prod_, which uses the
previously built image and exposes its HTTP port on port _5009_
of the host system, run the following command:
```shell
  $ docker run --name tea-prod -d -p 5009:5001 tea
```

Port _5001_ is the internal listening port for incoming HTTP
traffic, this port needs to be exposed to the host system on any free
port. The above example shows _5009_ on the host system, of course
any other port can be chosen as well.

### Reverse Proxy
Example _nginx_ webserver config for reverse-proxying to the above-mentioned container. HSTS headers included. 
```
server {
        listen <ip-v4> ssl http2;
        listen <ip-v6>:443 ssl http2;

        server_name <hostname>;

        ssl_certificate <tls-cert-path>;
        ssl_certificate_key <tls-private-key-path>;

        location / {
            proxy_hide_header Strict-Transport-Security;
            add_header Strict-Transport-Security "max-age=31536000; preload";

            proxy_pass http://<target-machine>:5009/;
        }    
    }
```