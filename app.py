from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_ip = request.form.get('ip_address')

        # Validate the input to prevent dangerous substrings
        forbidden_substrings = ["grep", "while", "read", "'",  "ls", "cat", "less", "tail", "more",
                                "whoami", "pwd", "busybox", "echo",
                                " ", "&", "!", "@", "%", "^", "~", "`",
                                "<", ">", ",", "\\", "/"]
        if any(substring in input_ip for substring in forbidden_substrings):
            output = "Input contains forbidden characters or commands."
        else:
            try:
                # Dangerous: Using os.system to execute command
                os.system(f"ping -c 1 {input_ip} > /tmp/result.txt")
                with open("/tmp/result.txt", "r") as file:
                    output = file.read()
            except Exception as e:
                output = f"An error occurred: {e}"

        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Ping Result</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #f3f4f6, #dbe2e6);
                        text-align: center;
                        margin: 0;
                        padding: 0;
                        color: #333;
                    }
                    h1 {
                        color: #1e90ff;
                        margin-top: 20px;
                        font-size: 2.5rem;
                    }
                    p {
                        font-size: 1.1rem;
                    }
                    pre {
                        background: #fff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        margin-top: 20px;
                        font-size: 1rem;
                        white-space: pre-wrap;
                        text-align: left;
                        display: inline-block;
                    }
                    a {
                        text-decoration: none;
                        color: #1e90ff;
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
                <h1>Ping Result</h1>
                <p>Here is the result for the IP address <strong>{{ input_ip }}</strong>:</p>
                <pre>{{ output }}</pre>
                <a href="/">Try Another IP</a>
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
                    background: linear-gradient(135deg, #f3f4f6, #dbe2e6);
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    color: #333;
                }
                h1 {
                    color: #1e90ff;
                    margin-top: 20px;
                    font-size: 2.5rem;
                }
                p {
                    font-size: 1.2rem;
                }
                form {
                    margin-top: 30px;
                    padding: 20px;
                    background: #fff;
                    border-radius: 10px;
                    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                    display: inline-block;
                }
                label {
                    display: block;
                    margin-bottom: 10px;
                    font-size: 1.1rem;
                    color: #555;
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
                    background-color: #1e90ff;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-top: 10px;
                }
                input[type="submit"]:hover {
                    background-color: #4682b4;
                }
            </style>
        </head>
        <body>
            <h1>Network Utility Tool</h1>
            <p>Enter an IP address to check connectivity:</p>
            <form method="post">
                <label for="ip_address">IP Address:</label>
                <input type="text" name="ip_address" id="ip_address" placeholder="e.g., 1.1.1.1" required>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    # Start the Flask application
    app.run(host='0.0.0.0', port=5000)
