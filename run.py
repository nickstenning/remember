import os
import remember

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    app = remember.create_app()
    app.run(port=port, host=host)
