# Nordlys

Entities (such as people, organizations, or products) are meaningful units for organizing information and can provide direct answers to many search queries.  Nordlys is a toolkit for entity-oriented and semantic search. 


## Functionality

Nordlys currently supports four entity-oriented tasks, which are core components in semantic search:

- Entity cataloging
- Entity retrieval
- Entity linking in queries
- Target type identification


## Features

- General-purpose information retrieval and machine learning components at its core
- Implementations of various methods for the above entity-oriented search tasks (with more on their way)
- Based on the DBpedia knowledge base (extendible to other knowledge bases)
- Can used as a black box through a [RESTful API](http://api.nordlys.cc/)
- Can be reached via a [graphical web user interface](http://gui.nordlys.cc/)
- Can be deployed on a local server and used as a Python package or as a command line tool
- Highly modular and [well documented](http://nordlys.readthedocs.io/) code, based on a 3-tier architecture
- Open source project that is actively being developed


## Disclaimer

Nordlys is not (yet) a mature production-level system, but rather a research prototype (as can be seen from the current version number, which is v0.2).  We welcome contributions on all levels (pull requests, suggestions for improvements, feature requests, etc.).

## Conference article

Nordlys was presented as the following conference article:

> F. Hasibi, K. Balog, D. Garigliotti and S. Zhang. **Nordlys: A Toolkit for Entity-Oriented and Semantic Search.** In: Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '17). ACM. Tokyo, Japan. August 2017. [DOI: 10.1145/3077136.3084149](https://doi.org/10.1145/3077136.3084149)

**You can get the author version of the article [here](http://krisztianbalog.com/files/sigir2017-nordlys.pdf).**

If you use the resources presented in this repository, please cite:

```
@inproceedings{Hasibi:2017:NTE,
 author = {Hasibi, Faegheh and Balog, Krisztian and Garigliotti, Dar\'{\i}o and Zhang, Shuo},
 title = {Nordlys: A Toolkit for Entity-Oriented and Semantic Search},
 booktitle = {Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval},
 series = {SIGIR '17},
 year = {2017},
 pages = {1289--1292},
 doi = {10.1145/3077136.3084149},
 publisher = {ACM},
}
```

If possible, please also include the http://nordlys.cc/ URL in your paper.


## Contributors

[Faegheh Hasibi](http://hasibi.com/), [Krisztian Balog](http://krisztianbalog.com), [Dario Garigliotti](https://dariogarigliotti.github.io), [Shuo Zhang](https://www.uis.no/article.php?articleID=109646&categoryID=11198).

