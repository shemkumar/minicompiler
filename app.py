from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

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
                font-family: 'Courier New', monospace;
                background: #111;
                color: #00ff00;
                margin: 0;
                padding: 0;
            }

            .container {
                width: 80%;
                max-width: 900px;
                margin: 50px auto;
                background: rgba(0, 0, 0, 0.8);
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
                text-align: center;
                animation: glow 1.5s ease-in-out infinite alternate;
            }

            h1 {
                font-size: 2.5em;
                color: #ff6347;
                margin-bottom: 20px;
                text-shadow: 0 0 5px #ff6347, 0 0 10px #ff6347;
            }

            p {
                font-size: 1.2em;
                color: #7fff00;
                margin-bottom: 20px;
                line-height: 1.5;
            }

            textarea {
                width: 100%;
                height: 200px;
                padding: 15px;
                background: #222;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 8px;
                font-size: 1.2em;
                font-family: 'Courier New', monospace;
                margin-top: 20px;
                transition: 0.3s ease-in-out;
            }

            textarea:focus {
                background: #333;
                outline: none;
                box-shadow: 0 0 10px #00ff00;
            }

            button {
                display: inline-block;
                width: 100%;
                padding: 12px;
                background: #00ff00;
                color: #111;
                border: none;
                border-radius: 5px;
                font-size: 1.4em;
                cursor: pointer;
                margin-top: 20px;
                transition: background 0.3s ease-in-out;
            }

            button:hover {
                background: #32cd32;
            }

            footer {
                margin-top: 40px;
                font-size: 1.2em;
                color: #7fff00;
            }

            @keyframes glow {
                0% {
                    box-shadow: 0 0 10px #ff6347, 0 0 20px #ff6347;
                }
                100% {
                    box-shadow: 0 0 20px #ff6347, 0 0 40px #ff6347;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Mini Compiler - Fun with Python</h1>
            <p>Hack Our Compiler Get the Job Offer!</p>
            <form action="/compile" method="post">
                <textarea name="code" placeholder="Write your Python code here..."></textarea><br>
                <button type="submit">Compile & Run</button>
            </form>
            <footer>
                <p>Mini Compiler Challenge - 2024 | Developed By Sam </p>
            </footer>
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
    app.run(debug=True, host='0.0.0.0')
