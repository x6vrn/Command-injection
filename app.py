from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_ip = request.form.get('ip_address')
        
        forbidden_substrings = ["while", "'", "ls", "cat", "tail", "more",
                                "whoami", "pwd", "busybox", "echo",
                                " ", "&", "!", "@", "%", "^", "~", "`",
                                "<", ">", ",", "\\", "/"]
        if any(substring in input_ip for substring in forbidden_substrings):
            output = "Your input contains invalid characters or commands. Please try again."
        else:
            try:
                os.system(f"ping -c 1 {input_ip} > /tmp/result.txt")
                with open("/tmp/result.txt", "r") as file:
                    output = file.read()
            except Exception as e:
                output = f"Oops! Something went wrong: {e}"

        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Scan Results</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: #1b1b1b;
                        color: #f2f2f2;
                        text-align: center;
                        margin: 0;
                        padding: 0;
                    }
                    h1 {
                        color: #ff6f61;
                        margin-top: 20px;
                        font-size: 2.5rem;
                    }
                    p {
                        font-size: 1.1rem;
                    }
                    pre {
                        background: #2a2a2a;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
                        margin-top: 20px;
                        font-size: 1rem;
                        white-space: pre-wrap;
                        text-align: left;
                        display: inline-block;
                        color: #ffd966;
                    }
                    a {
                        text-decoration: none;
                        color: #ff6f61;
                        font-weight: bold;
                        display: block;
                        margin-top: 20px;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <h1>Ping Check Results</h1>
                <p>Below are the connectivity details for <strong>{{ input_ip }}</strong>:</p>
                <pre>{{ output }}</pre>
                <a href="/">Test Another IP</a>
            </body>
            </html>
        ''', input_ip=input_ip, output=output)

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Network Utility</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: #1b1b1b;
                    color: #f2f2f2;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    color: #ff6f61;
                    margin-top: 20px;
                    font-size: 2.5rem;
                }
                p {
                    font-size: 1.2rem;
                }
                form {
                    margin-top: 30px;
                    padding: 20px;
                    background: #2a2a2a;
                    border-radius: 10px;
                    box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
                    display: inline-block;
                }
                label {
                    display: block;
                    margin-bottom: 10px;
                    font-size: 1.1rem;
                    color: #ffd966;
                }
                input[type="text"] {
                    padding: 10px;
                    font-size: 16px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                    width: 100%;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    background-color: #ff6f61;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-top: 10px;
                }
                input[type="submit"]:hover {
                    background-color: #e25447;
                }
            </style>
        </head>
        <body>
            <h1>Network Connectivity Tool</h1>
            <p>Enter an IP address to check for network connectivity:</p>
            <form method="post">
                <label for="ip_address">Target IP Address:</label>
                <input type="text" name="ip_address" id="ip_address" placeholder="Example: 8.8.8.8" required>
                <input type="submit" value="Run Check">
            </form>
        </body>
        </html>
    ''')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
