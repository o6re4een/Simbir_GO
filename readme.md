Installation:

Prereq: 
    docker-desktop
    

Configuration:
    create .env in root 
    configure it like in .sample.env
    POSTGRES_PORT leave as default 5435
    POSTGRES_HOST leave as default too

adding Admin:
    JWT_SECRET is a secret for /api/Admin/Create

Run: 
    docker-compose build 

    docker-compose up
