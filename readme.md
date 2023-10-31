# Simbir_GO rent backend

## Installation

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Configuration
1. Create a `.env` file in the project root directory.
2. Configure the `.env` file based on the provided `.sample.env` file.
    - Ensure `POSTGRES_PORT` is set to the default value, which is `5435`.
    - Leave `POSTGRES_HOST` at its default value.

### Adding an Admin
- `JWT_SECRET` is a secret required for the `/api/Admin/Create` operation.

## Run

1. Build the project with Docker:
    ```bash
    docker-compose build
    ```

2. Start the project with Docker:
    ```bash
    docker-compose up
    ```

## License
This project is licensed under the [MIT License](LICENSE).