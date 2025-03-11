from flask import Flask

print("Starting Flask app...")  # Debugging
app = Flask(__name__)

print("Running Flask...")
if __name__ == '__main__':
    app.run(debug=True)