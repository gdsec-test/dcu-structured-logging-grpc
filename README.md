# dcu-structured-logging-grpc

Configure the gRPC interceptor as described below.

## Example
```py
from dcustructuredlogginggrpc import get_logging, LoggerInterceptor

# A bunch of important code that will make the below calls work.

if __name__ == '__main__':
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10), interceptors=[LoggerInterceptor()])
    pb.phishstory_service_pb2_grpc.add_PhishstoryServicer_to_server(
        API(), server)
    logger.info("Listening on port 50051...")
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        logger.info("Stopping server")
        server.stop(0)
```