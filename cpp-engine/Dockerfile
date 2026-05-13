FROM alpine:3.20 AS builder
RUN apk add --no-cache cmake g++ make openssl-dev
WORKDIR /build
COPY . .
RUN mkdir build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)

FROM alpine:3.20
RUN apk add --no-cache libstdc++ openssl
COPY --from=builder /build/build/kavach /usr/local/bin/kavach
COPY rules/ /etc/kavach/rules/
EXPOSE 8000
CMD ["kavach"]
