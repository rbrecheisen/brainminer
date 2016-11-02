# Design

## Modules

The application consists of 3 main modules:

  - auth
  - compute
  - storage
    
### Auth
The auth module is responsible for authenticating and authorizing users.
It also handles permission checking, i.e., authorization of users when
they attempt to access certain resources.

### Compute
The compute module is responsible for executing processing pipelines. It
relies on an asynchronous task queue.

### Storage
The storage module is responsible for storage and retrieval of files as
well as organizing files in repositories and file sets. Physical file
upload and download is handled by a Nginx webserver. The webserver runs
inside a Docker container.

## Database

Each module is associated with a number of database tables containing 
meta information, e.g., about users, user groups, files, repositories
and file sets. The database is implemented using PostgreSQL and runs 
inside a Docker container.