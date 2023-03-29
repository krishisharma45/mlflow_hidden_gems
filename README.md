<h1>MLFlow Hidden Gems</h1>

A containerized image recognition application that demonstrates some core capabilities within MLFlow.

[Python 3.8][python-url]

### Requirements

- [Docker][docker-url]
- [Docker Compose][docker-compose-url]
- [NVIDIA Docker Container Runtime][nvidia-url]

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for
development and testing purposes.

Docker is used to ensure consistency across development, test, training, and production
environments. The Docker image is fully self-contained, so all required frameworks and libraries
will be installed as part of the image creation process.

### First Time Users

If this is your first time using this application, please ensure that you have installed the
[requirements](#requirements) listed above before proceeding. Also make sure that you create a .env file from the .env.example template. If you are using MacOS or Linux, you
can run this command:

```sh
brew install git docker pre-commit shellcheck
```

On Windows you can run this commmand:

```sh
choco install git docker pre-commit shellcheck
```

We use pre-commit, a package manager for pre commit hooks, to run a list of hooks that checks the
following criteria before allowing a user to commit their changes:

- files parse as valid Python
- commit contains files less than 100MB in size
- commit does not contain any private key
- ensures that a file is either empty, or ends with one newline
- sorts entries in requirements.txt
- trims trailing whitespace
- runs black, a Python code formatter

To ensure that pre-commit is used, run

```sh
pre-commit install
```

after git, docker and pre-commit are installed from the previous step above. This will ensure that
pre-commit always runs the list of hooks defined in the .pre-commit-config.yaml file in the
project's root directory.

To get started, start playing with some of the [commands](#summary-of-commands) or [launch the
application locally](#launching-the-application).

### Launching the Application

To launch this application, you need to first create a .env file for this project. Please use the .env.example to help you build your .env file. Then, you need to build the Docker image using

```sh
bin/build.sh
```

and then bring up the containers for the application with

```sh
bin/up.sh
```

<u>Note</u>: To bring up a particular service, specify the service name (name given in Docker
Compose). For example, to bring up just the MLFlow service and not the app, you can run:

```sh
bin/up.sh mlflow
```

Once you're done working with your application, you can stop all containers and remove the
containers, volumes and images associated with the application by running:

```sh
bin/down.sh
```

Below are additional instruction on [training](#training) and [running tests](#testing) to verify
that everything is working.

## Additional Commands
### Training

To train the model, all you need to do is run this command:

```sh
bin/train.sh
```

(Note: Please include further instructions if GPU is required!)

### Testing

Once the Docker image is built we can run the project's unit tests to verify everything is
working. The below command will start a Docker container and execute all unit tests using the
[pytest framework](https://docs.pytest.org/en/latest/).

```sh
bin/test.sh
```


### Summary of Commands

The `bin/` directory contains basic shell bin that allow us access to common commands on most
environments. We're not guaranteed much functionality on any generic machine, so keeping these
basic is important.

The most commonly used bin are:

- `bin/build.sh` - build docker container(s) defined in `Dockerfile` and `docker-compose.yml`
- `bin/test.sh` - run unit tests defined in `tests/`
- `bin/shell.sh` - instantiate a new bash terminal inside the container
- `bin/train.sh` - train a model

Additional bin:

- `bin/setup_environment.sh` - sets any build arguments or settings for all containers brought up
  with docker-compose
- `bin/up.sh` - bring up all containers defined in `docker-compose.yml`
- `bin/down.sh` - stops all containers defined in `docker-compose.yml` and removes associated
  volumes, networks and images

#### Example of How to Use the Commands

If you want to use the shell script for a specific service listed in your Docker Compose, then you
can do that by listing the name of the service after the shell script.

For example, if we wanted to specifically use the shell script to inspect the MLFlow container of
an application, we can run:

```sh
bin/shell.sh mlflow
```

Note that this assumes that there is a service in the Docker Compose called "mlflow".

## Data Directory

Data organization philosophy from [cookiecutter data
science](https://github.com/drivendata/cookiecutter-data-science)

```
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
```

Note: this directory will often be backed up with a blob store (e.g. S3) or a shared mounted drive
(e.g. EFS).

[license-url]: ./LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/kungfuai/
[python-url]: https://www.python.org
[docker-url]: https://www.docker.com
[docker-compose-url]: https://docs.docker.com/compose/install/
[nvidia-url]: https://github.com/NVIDIA/nvidia-container-runtime
[kungfu-shield]: https://img.shields.io/badge/KUNGFU.AI-2022-red
[kungfu-url]: https://www.kungfu.ai
