from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

FLAG = "CTF{mini_compiler_pwn}"

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mini Compiler</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #2c3e50, #3498db);
                color: #ecf0f1;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 80%;
                max-width: 800px;
                margin: 50px auto;
                background: rgba(44, 62, 80, 0.9);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
                font-size: 2em;
                color: #1abc9c;
            }
            p {
                text-align: center;
                font-size: 1.1em;
            }
            textarea {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                border: none;
                border-radius: 5px;
                font-family: monospace;
                font-size: 1em;
            }
            button {
                display: block;
                width: 100%;
                padding: 10px;
                background: #1abc9c;
                color: #fff;
                border: none;
                border-radius: 5px;
                font-size: 1.2em;
                cursor: pointer;
            }
            button:hover {
                background: #16a085;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Mini Compiler</h1>
            <p>This tool allows you to submit Python code and see its output. Be creative, but play fair!</p>
            <form action="/compile" method="post">
                <textarea name="code" rows="10" cols="50" placeholder="Write your Python code here..."></textarea><br>
                <button type="submit">Compile & Run</button>
            </form>
        </div>
    </body>
    </html>
    ''')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.form.get('code', '')

    # Save code to a temporary file
    temp_file = 'temp_code.py'
    with open(temp_file, 'w') as f:
        f.write(code)

    try:
        # Dangerous: Executes the user's code directly
        result = subprocess.check_output(['python3', temp_file], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        result = f"Error: {e.output}"
    finally:
        # Clean up the temporary file
        os.remove(temp_file)

    return f"<pre>{result}</pre>"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

