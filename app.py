from website import create_app

app = create_app()
# if we run this file, we will execute this line
if __name__ == "__main__":
    app.run(debug=True)

