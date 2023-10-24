Ouihelp's Secret Santa
===
A group of demanding friends gather for Christmas and would like to exchange gifts anonymously.

Write a piece of software that processes the list of participants so each person knows who make
a gift to. The friends are picky so the software must abide by these rules:
1. each person must make and receive exactly one gift;
2. a recipient does not make a gift to his source;
3. couples must not give gifts to one another.

# Data sets
The “couple contraint” is considered as a generic “exclusion constraint” so it's easier to extend
it later.

## Building a graph

1. build a graph of all possible assignments
2. find a connected path that goes through everyone
    * backtrack whenever a path is not valid

## issues
* If someone has only one valid recipient option, we must make sure this option is not given to
someone else (someone with more than one option).

# Script presentation

# Run it
First build the Docker image, then run it.
```shell
docker build -t ouihelp_secret_santa:dev .
docker run --rm ouihelp_secret_santa:dev
```

# Tests
```shell
python -m unittest discover -s secret_santa/ --failfast -vv
```

# How to improve?

# Issues
