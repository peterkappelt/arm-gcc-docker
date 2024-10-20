FROM debian:bookworm-slim

ARG GCC_FOLDER TARGETARCH
RUN test -n "$GCC_FOLDER" || (echo "GCC_FOLDER  not set" && false)

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends build-essential wget libncursesw5 zlib1g-dev ca-certificates
RUN DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends cmake ninja-build
RUN DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends git-core
RUN DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends bash zsh sudo

RUN mkdir /compiler
COPY "./gcc_$TARGETARCH/$GCC_FOLDER" "/compiler/$GCC_FOLDER"

RUN bash -c "chmod +x /compiler/$GCC_FOLDER/bin/*"

ENV PATH "/compiler/$GCC_FOLDER/bin:$PATH"

# GDB requires python3.8 for some reason, so install it
RUN mkdir /python_build
RUN wget https://www.python.org/ftp/python/3.8.17/Python-3.8.17.tgz -O /python_build/python.tgz
RUN tar xzvf /python_build/python.tgz -C /python_build
RUN bash -c 'cd /python_build/Python-3.8.17 && ./configure && make && make install'
RUN rm -r /python_build

RUN mkdir /work
WORKDIR /work
