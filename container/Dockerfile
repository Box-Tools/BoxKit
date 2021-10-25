# Dockerfile

ARG maple_image
FROM ${maple_image}

MAINTAINER adhruv

ARG maple_target
WORKDIR ${maple_target}

CMD ["sh", "-c", "cd cbox/src && make && cd ../../ && \
                  python3 setup.py develop --user && \
                  python3 tests/library/create.py"]
