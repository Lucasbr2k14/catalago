from app import create_app
from configs import Configs

configs = Configs()
app = create_app(configs)

if __name__ == "__main__":
    app.run(
        host=configs.host,
        port=configs.port,
        debug=configs.dev
    )