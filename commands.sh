python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/clock.proto --pyi_out=.

protoc --js_out=import_style=commonjs,binary:. --grpc-web_out=import_style=commonjs,mode=grpcweb:. clock.proto --decode=MESSAGE_TYPE




