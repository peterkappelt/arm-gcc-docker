FROM alpine:latest

ARG GCC_FOLDER
RUN test -n "$GCC_FOLDER" || (echo "GCC_FOLDER  not set" && false)

RUN apk update
RUN apk add bash
RUN apk add build-base wget cmake
#gcompat is required for libc compatibility
RUN apk add gcompat 

RUN mkdir /compiler
COPY "./$GCC_FOLDER" "/compiler/$GCC_FOLDER"

RUN bash -c "chmod +x /compiler/$GCC_FOLDER/bin/*"

ENV PATH "/compiler/$GCC_FOLDER/bin:$PATH"

RUN mkdir /work
WORKDIR /work