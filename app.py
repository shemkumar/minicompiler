from flask import Flask, request, render_template_string
import subprocess
import os
import sys

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

    result = ""
    try:
        # Execute the user's code in a restricted environment using a separate process
        # This is still not a full sandbox, but it's an improvement over direct execution.
        # For true security, consider a containerized environment or a dedicated sandbox library.
        python_executable = sys.executable # Use the current Python interpreter
        
        # We're adding a basic timeout to prevent infinite loops and limiting memory (if supported by OS)
        # This is still not a full sandbox, but it's an improvement over direct execution.
        # For true security, consider a containerized environment or a dedicated sandbox library.
        # The 'ulimit' command is specific to Unix-like systems and might not work on Windows.
        # A more robust solution would involve a dedicated sandbox library or containerization.
        command = [python_executable, temp_file]
        
        # Using Popen for more control, including preexec_fn for ulimit (Unix-only)
        # Note: preexec_fn is not available on Windows.
        if sys.platform != "win32":
            def set_limits():
                # Set CPU time limit to 5 seconds
                import resource
                resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
                # Set memory limit to 128MB (soft and hard limit)
                resource.setrlimit(resource.RLIMIT_AS, (128 * 1024 * 1024, 128 * 1024 * 1024))
            
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=set_limits)
        else:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            stdout, stderr = process.communicate(timeout=10) # 10 second timeout for execution
            if stdout:
                result += stdout
            if stderr:
                result += f"Error: {stderr}"
            if process.returncode != 0 and not stderr: # If there was an error but no stderr output
                result += f"Process exited with non-zero status: {process.returncode}"
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            result = f"Error: Execution timed out after 10 seconds.\n{stdout}\n{stderr}"
        
    except Exception as e:
        result = f"An unexpected error occurred: {e}"
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return f"<pre>{result}</pre>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
