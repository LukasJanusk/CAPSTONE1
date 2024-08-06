from dataclasses import dataclass


@dataclass
class Settings:
    draw_hitboxes = False
    draw_health_bar = False
    limit_particles = False


settings = Settings()
