# How to contribute

First off, thanks for taking an interest in this project. We are glad
about usage, ideas, and contributions to help us develop something 
everyone enjoys using.

For general questions and unstructured discussion, come see us in our 
[chat room](https://gitter.im/stenotype/community). 


## Resources

  * The [project board](https://github.com/a-recknagel/stenotype/projects/1) 
    shows the current roadmap and the progress on specific issues
  * The project docs on [github pages](https://a-recknagel.github.io/stenotype/)
  * [PEP 484](https://www.python.org/dev/peps/pep-0484/) introduced 
    type hinting to python
  * [PEP 526](https://www.python.org/dev/peps/pep-0526/),
    [PEP 544](https://www.python.org/dev/peps/pep-0544/),
    [PEP 560](https://www.python.org/dev/peps/pep-0560/),
    [PEP 563](https://www.python.org/dev/peps/pep-0563/), and
    [PEP 586](https://www.python.org/dev/peps/pep-0586/) extended it
  * [mypy](http://www.mypy-lang.org/) is used as reference for type
    annotation checks


## Development Quick Start
[Install poetry](https://poetry.eustace.io/docs/#installation) and run
`poetry install` in the project root. This will perform a dev-install of
the project in a new virtual environment, which should be all you need
to do to start contributing.

If your shell can't find the virtual env on its own, run `poetry shell`,
after which all tools and the `stenotype` cli should work properly.


## CI pipeline

Any pull request needs to pass 
[the CI](https://github.com/a-recknagel/stenotype/actions?workflow=CI-CD)
before it can be merged. The most important ones are formatting (`black
src/ tests/`), unit tests (`pytest tests/`), and static typing (`mypy
src/`), be sure to run those commands locally before every push.

For details, check the 
[tooling](https://a-recknagel.github.io/stenotype/tooling.html) section
of the docs.


## Submitting Changes

In general, pull requests should happen to solve an issue with the
project. Any content-related discussion regarding the issue should take
place on the issue itself, and comments on the pull request should all
broadly fall under
[code-review guidelines](https://mtlynch.io/human-code-reviews-1/).

An issue can be created for any of the following cases:

 - <span style="background-color:#D73A4A;color:#FBEEEB">bug</span> -
   make sure it is reproducible
 - <span style="background-color:#A2EEEF;color:#252525">enhancement</span> -
   aka feature request
 - <span style="background-color:#D876E3;color:#252525">question</span> - 
   whatever you feel like asking
 
If you plan to write one, please take care that yours falls among them 
and tag it accordingly.
