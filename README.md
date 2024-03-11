# Comments SPA application

Django project for managing comments in SPA application

## Installation

Before starting, you must have Docker installed

```shell
git clone https://github.com/Yevheniy-Lototskiy/py-comments.git
```

## Using

When the project is successfully installed, run these commands in Terminal:

```shell
docker-compose build
docker-compose up
```
 Then you can open your browser, and go to the address: [127.0.0.1:8001/comments](127.0.0.1:8001/comments)

To view all endpoints, go to the address: [127.0.0.1:8001/doc/swagger](127.0.0.1:8001/doc/swagger)
 
## Features
- CRUD operations with comments
- Pagination
- Filtering by values or fields
- CAPTCHA
- WebSocket
- Redis
- Swagger
