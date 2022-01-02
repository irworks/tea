from app.start import create_app
from waitress import serve

application = create_app()

if __name__ == '__main__':
    serve(application, host="0.0.0.0", port=5001)
