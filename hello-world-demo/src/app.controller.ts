import { Controller, Get } from '@nestjs/common';
import { AppService } from './app.service';
import { HelloService } from './hello/hello.service';
import { GrpcMethod } from '@nestjs/microservices';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService,
    private readonly helloService: HelloService
  ) {}

  @Get("/hel")
  getHello(): string {
    return this.appService.getHello();
  }

  @GrpcMethod('HelloService', 'SayHello')
  sayHello(data: any): { message: string } {
    return this.helloService.sayHello(data)
  }
}
