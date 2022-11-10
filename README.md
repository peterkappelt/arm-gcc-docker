# arm-none-eabi-gcc Docker Container

This repo contains scripts to build docker containers for the `arm-none-eabi-gcc`

## Usage

For compiling your project, you simply need to run the container while mounting your project dir in the container:

```
docker run \
  --rm \
  -v $(pwd):/work \
  ghcr.io/peterkappelt/arm-gcc-docker:10.3-2021.10 \
  make
```

## Included packages

The docker containers include:
 - the full `arm-gcc-none-eabi` suite
 - make
 - cmake

## Supported versions

Currently, containers for the following versions are available: 
  - 8-2018-q4-major
  - 9-2019-q4-major
  - 10-2020-q4-major
  - 10.3-2021.10

New gcc versions can be adding by providing their download URL in `fetch-armgcc.py` and adding a matrix build step in the Github workflow. Feel free to create a PR for that.

## Licensing

Though this build utility is licensed with MIT, `arm-none-eabi-gcc` is distributed with the GPLv3 license.