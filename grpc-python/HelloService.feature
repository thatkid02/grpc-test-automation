
Feature: Get HelloService

@GetHelloService
Scenario: To test the HelloService service
    Given def payload = "{'name': '#(__arg.name)'}"
    * def modifiedPayload = base.removeNullOr EmptyKeys(payload)
    * string payload = modifiedPayload
    * def client = new GrpcClient("grpcPortfolioServer", 443)
    * def response = client.call('hello.HelloService/SayHello', payload, karate)
