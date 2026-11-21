terraform {
    required_providers {
        render = {
            source  = "render-oss/render"
            version = "1.9.1"
        }
    }
}

provider "render" {}

resource "render_web_service" "api" {
    name   = "house-price-api"
    plan   = "free"
    region = "frankfurt"

    health_check_path = "/health"

    runtime_source = {
        docker = {
            repo_url        = "https://github.com/Kutlay07/house-price-ml-system"
            branch          = "main"
            dockerfile_path = "./Dockerfile"
            auto_deploy     = true
        }
    }
}
