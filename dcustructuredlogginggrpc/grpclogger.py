import datetime
import logging
import os
import time

import grpc
from grpc_interceptor import ServerInterceptor
from pythonjsonlogger import jsonlogger

from dcustructuredlogginggrpc.converter import protobuf_to_dict


class GrpcJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(GrpcJsonFormatter, self).add_fields(
            log_record, record, message_dict
        )
        log_record['timestamp'] = datetime.datetime.utcnow()


def get_logging():
    if len(logging.Logger.root.handlers) == 0:
        logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO').upper())
        logger = logging.getLogger()
        logger.handlers = []
        logHandler = logging.StreamHandler()
        formatter = GrpcJsonFormatter()
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
    return logging


class LoggerInterceptor(ServerInterceptor):

    def intercept(self, method, request, context, method_name):
        start = time.time()
        try:
            result = method(request, context)
        finally:
            result_dict = {}
            request_dict = protobuf_to_dict(
                request,
                including_default_value_fields=True
            )
            status_code = grpc.StatusCode.OK.value[0]
            if result:
                result_dict = protobuf_to_dict(
                    result,
                    including_default_value_fields=True
                )
            if context._state.code and len(context._state.code.value) > 0:
                status_code = context._state.code.value[0]

            data = {
                'grpc-info': {
                    'status': status_code,
                    'method': method_name,
                    'duration': time.time() - start,
                    'request-body': request_dict,
                    'response-body': result_dict
                }
            }

            if request_dict.get('ticketId'):
                data['ticketId'] = request_dict.get('ticketId')

            get_logging().info('Request processed', extra=data)
        return result
