import grpc
import logging
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc
from google.protobuf import descriptor_pb2

logging.basicConfig(level=logging.DEBUG)

def list_services(host, port):
    """
    A function that lists services available on a given host and port.

    Parameters:
    - host (str): The host address.
    - port (int): The port number.

    Returns:
    - list: A list of service names available.
    """
    channel = grpc.insecure_channel(f"{host}:{port}")
    try:
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)
        service_names = []
        for response in stub.ServerReflectionInfo(iter_requests(list_services="")):
            if response.HasField("list_services_response"):
                for service in response.list_services_response.service:
                    service_names.append(service.name)
            else:
                logging.warning("Response does not contain list_services_response.")
        return service_names
    except grpc.RpcError as e:
        logging.error(f"Error: {e}")
        return None
    finally:
        channel.close()
        
def get_proto_details(host, port, service_name):
    """
    A function to retrieve details from a gRPC server reflection service.

    Parameters:
    - host (str): The host address of the gRPC server.
    - port (int): The port number of the gRPC server.
    - service_name (str): The name of the service to retrieve details for.

    Returns:
    - list: A list of service names retrieved from the server reflection.
    """
    channel = grpc.insecure_channel(f"{host}:{port}")
    try:
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)
        service_names = []
        for response in stub.ServerReflectionInfo(iter_requests(file_containing_symbol=f'{service_name}')):
            if response.HasField("file_descriptor_response"):
                for service in response.file_descriptor_response.file_descriptor_proto:
                    service_names.append(service)
            else:
                logging.warning("Response does not contain list_services_response.")
        return service_names
    except grpc.RpcError as e:
        logging.error(f"Error: {e}")
        return None
    finally:
        channel.close()
    

def iter_requests(list_services=None, file_containing_symbol=None):
    """
    This function generates requests based on the provided list of services and file containing a symbol.
    
    Args:
        list_services (list): A list of services to generate requests for. Defaults to None.
        file_containing_symbol (str): The file containing the symbol for which a request should be generated. Defaults to None.
        
    Yields:
        reflection_pb2.ServerReflectionRequest: A ServerReflectionRequest based on the input parameters.
    """
    if file_containing_symbol:
        yield reflection_pb2.ServerReflectionRequest(file_containing_symbol=file_containing_symbol)
    else:
        yield reflection_pb2.ServerReflectionRequest(list_services="")


def parse_proto(proto_details):
    """
    Parse the given proto_details to extract file name, package name, and services with their methods, requests, and responses.
    """
    file_desc_proto = descriptor_pb2.FileDescriptorProto.FromString(proto_details)

    proto_obj = {
        'file_name': file_desc_proto.name,
        'package_name': file_desc_proto.package,
        'services': []
    }

    for service in file_desc_proto.service:
        service_obj = {'service_name': service.name, 'methods': []}

        for method in service.method:
            method_obj = {'method_name': method.name}

            # request_obj = {'name': method.input_type.split('.')[-1], 'fields': []}
            request_obj = {}
            for message_type in file_desc_proto.message_type:
                if message_type.name == method.input_type.split('.')[-1]:
                    for field in message_type.field:
                        request_obj[field.name] = f'#(__arg.{field.name})'
                    break

            # response_obj = {'name': method.output_type.split('.')[-1], 'fields': []}
            response_obj = {}
            response_obj['fields'] = []
            for message_type in file_desc_proto.message_type:
                if message_type.name == method.output_type.split('.')[-1]:
                    for field in message_type.field:
                        response_obj['fields'].append({
                            'name': field.name,
                            'type': descriptor_pb2.FieldDescriptorProto.Type.Name(field.type)
                        })
                    break

            method_obj['request'] = request_obj
            method_obj['response'] = response_obj

            service_obj['methods'].append(method_obj)

        proto_obj['services'].append(service_obj)

    return proto_obj

def create_feature_file(proto_obj):
    """
    A function to create feature files based on the provided proto object.
    
    Parameters:
        proto_obj (dict): A dictionary containing information about services and methods.
    
    Returns:
        None
    """
    for service in proto_obj['services']:
        karate_feature = f"""
Feature: Get {service['service_name']}

@Get{service['service_name']}
Scenario: To test the {service['service_name']} service
    Given def payload = "{service['methods'][0]['request']}"
    * def client = new GrpcClient("localhost", 5000)
    * def response = client.call('{proto_obj['package_name']}.{service['service_name']}/{service['methods'][0]['method_name']}', payload, karate)
"""
        # write to file as service name.feature
        with open(f'{service["service_name"]}.feature', 'w') as f:
            f.write(karate_feature)
            
# If using TLS then use secure channel pass empty creds
# port might be 443
host = "localhost"
port = 5000
services = list_services(host, port)
if services:
    for service_name in services:
        proto_obj = (get_proto_details(host, port, service_name))[0]
        create_feature_file(parse_proto(proto_obj))
else:
    print("Failed to list services.")


