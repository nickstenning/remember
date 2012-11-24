from IPython import embed

import remember

def main():
    app = remember.create_app()

    with app.test_request_context():
        embed(display_banner=False)

if __name__ == '__main__':
    main()

