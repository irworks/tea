# tls-analyzer
[![Repo on GitLab](https://img.shields.io/badge/repo-GitLab-fc6d26.svg?style=flat&logo=gitlab)](https://git.mp-software.io/RUB-AI/bachelor-arbeit/tls-analyzer)
[![license](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE.md)
[![Python Version](https://img.shields.io/badge/python-3.7%20|%203.9-blue)](https://git.mp-software.io/RUB-AI/bachelor-arbeit/tls-analyzer)

Analyze iOS apps regarding [ATS](https://developer.apple.com/documentation/security/preventing_insecure_network_connections) exception and extract urls.   

### Usage
Prepare a folder containing `.ipa` files for analysis. To extract multiple apps at once you can use [ipdumper](https://gitlab.com/marzzzello/ipa-dumper).

### Parameters
Full example: `-v DEBUG -w /Users/ilja/Desktop/tls-analyzer-work-dir --output results.json`
#### Required
- `--work-dir` (`-w`)
  - Specify your working directory.

#### Optional
- `--verbosity` (`-v`) 
  - Log level, values: [`INFO, WARNING, DEBUG`]
  - **Default:** `INFO`
- `--output` (`-o`) 
  - Output file name and path
  - **Default:** `results.json`
- `--ignore-url-cache` (`-i`)
  - Set this flag if you want to rescan all apps for urls

### Output
Currently, the data is output as a `json` file.