# Dockerfile

ARG maple_image
FROM ${maple_image}

MAINTAINER adhruv

ARG maple_target
WORKDIR ${maple_target}

CMD ["sh", "-c", "./setup && \
                  python3 tests/container"]
