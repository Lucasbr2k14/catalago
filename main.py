from app import create_app
from configs import Configs

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    configs = Configs()

    app = create_app(
        configs
    )

    app.run(
        debug=True,
        port=configs.port,
        host=configs.host
    )
    