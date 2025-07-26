from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return open("index.html").read()

@app.route('/run-script')
def run_script():
    try:
        # Run the Python script without expecting any output
        subprocess.run(["python", "fed.py"], check=True)
        return "Detection process completed"
    except Exception as e:
        return f"Error running script: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
