FROM debian:bookworm-slim

ARG GCC_FOLDER TARGETARCH
RUN test -n "$GCC_FOLDER" || (echo "GCC_FOLDER  not set" && false)

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends bash build-essential wget cmake libncurses5 ninja-build

RUN mkdir /compiler
COPY "./gcc_$TARGETARCH/$GCC_FOLDER" "/compiler/$GCC_FOLDER"

RUN bash -c "chmod +x /compiler/$GCC_FOLDER/bin/*"

ENV PATH "/compiler/$GCC_FOLDER/bin:$PATH"

RUN mkdir /work
WORKDIR /work
