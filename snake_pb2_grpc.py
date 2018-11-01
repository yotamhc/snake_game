# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import snake_pb2 as snake__pb2


class SnakeServerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.JoinGame = channel.unary_unary(
        '/snake.SnakeServer/JoinGame',
        request_serializer=snake__pb2.ClientInfo.SerializeToString,
        response_deserializer=snake__pb2.Events.FromString,
        )
    self.KeyPress = channel.unary_unary(
        '/snake.SnakeServer/KeyPress',
        request_serializer=snake__pb2.KeyPressEvent.SerializeToString,
        response_deserializer=snake__pb2.Events.FromString,
        )
    self.Poll = channel.unary_unary(
        '/snake.SnakeServer/Poll',
        request_serializer=snake__pb2.PollRequest.SerializeToString,
        response_deserializer=snake__pb2.Events.FromString,
        )


class SnakeServerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def JoinGame(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def KeyPress(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Poll(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SnakeServerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'JoinGame': grpc.unary_unary_rpc_method_handler(
          servicer.JoinGame,
          request_deserializer=snake__pb2.ClientInfo.FromString,
          response_serializer=snake__pb2.Events.SerializeToString,
      ),
      'KeyPress': grpc.unary_unary_rpc_method_handler(
          servicer.KeyPress,
          request_deserializer=snake__pb2.KeyPressEvent.FromString,
          response_serializer=snake__pb2.Events.SerializeToString,
      ),
      'Poll': grpc.unary_unary_rpc_method_handler(
          servicer.Poll,
          request_deserializer=snake__pb2.PollRequest.FromString,
          response_serializer=snake__pb2.Events.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'snake.SnakeServer', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class SnakeClientStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.EventHandler = channel.unary_unary(
        '/snake.SnakeClient/EventHandler',
        request_serializer=snake__pb2.Events.SerializeToString,
        response_deserializer=snake__pb2.Ack.FromString,
        )


class SnakeClientServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def EventHandler(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SnakeClientServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'EventHandler': grpc.unary_unary_rpc_method_handler(
          servicer.EventHandler,
          request_deserializer=snake__pb2.Events.FromString,
          response_serializer=snake__pb2.Ack.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'snake.SnakeClient', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
