from website import create_app

app = create_app()

# only run webserver when ran from here directly
if __name__ == '__main__':
    app.run(debug=True)
