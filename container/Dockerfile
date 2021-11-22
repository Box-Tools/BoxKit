# Dockerfile

ARG maple_image
FROM ${maple_image}

MAINTAINER adhruv

ARG maple_target
WORKDIR ${maple_target}

CMD ["sh", "-c", "./setup develop && ./setup clean && python3 tests/container && \
                   /home/user/.local/bin/jupyter notebook --port=8888 --no-browser --ip=0.0.0.0"]
