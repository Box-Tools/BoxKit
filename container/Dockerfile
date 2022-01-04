# Dockerfile

ARG maple_image
FROM ${maple_image}

ARG maple_user
ARG maple_group
RUN addgroup --gid $maple_group user
RUN adduser --disabled-password --gecos '' --uid $maple_user --gid $maple_group user

USER user

ARG maple_target
WORKDIR ${maple_target}

CMD ["sh", "-c", "./setup develop && ./setup clean && python3 tests/container"]
