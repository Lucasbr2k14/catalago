from app import create_app
from configs import Configs

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    app = create_app(
        Configs()
    )

    app.run(
        debug=True,
        port=8080,
        host="0.0.0.0"
    )
    