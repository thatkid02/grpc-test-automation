import { Injectable } from '@nestjs/common';

@Injectable()
export class HelloService {
  sayHello(data: any): { message: string } {
    console.log("****************************", data)
    return { message: 'Hello, World!' };
  }
}