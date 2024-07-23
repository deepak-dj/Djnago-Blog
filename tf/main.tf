resource "docker_network" "blog_network" {
    name = "blog_network"
}

resource "docker_container" "db" {
    name = "db"
    image = "postgres"
    network_advanced {
      name = docker_network.blog_network.name
    }
    env = [
          "POSTGRES_DB=blog_db",
          "POSTGRES_USER=postgres",
          "POSTGRES_PASSWORD=root"
        ]
}

resource "docker_container" "blog_ctr" {
    name = "blog-app"
    image = "djdocker001/blog-app"
    network_advanced {
      name = docker_network.blog_network.name
    }
    env = [
              "DATABASE_NAME=blog_db",
              "DATABASE_USER=postgres",
              "DATABASE_PASSWORD="root",
              "DATABASE_HOST=db",
              "DATABASE_PORT=5432"
        ]
    ports {
        internal = 8000
        external = 8000
    }
}
  
