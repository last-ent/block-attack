from app import app

# uwsgi --socket 0.0.0.0:8000 --protol=http -w wsgi --callable app

if __name__ == '__main__':
    app.run()
