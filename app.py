from flask import Flask, request, render_template_string
import mysql.connector
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # change if needed
        password="",          # change if needed
        database="salary_db"
    )

# Predict salary using Linear Regression
def predict_salary(cgpa, experience):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT cgpa, experience, salary FROM user_data")
    data = cursor.fetchall()
    conn.close()

    if len(data) < 2:
        return 30000  # default fallback salary if not enough data

    X = np.array([[row[0], row[1]] for row in data])
    y = np.array([row[2] for row in data])

    model = LinearRegression()
    model.fit(X, y)
    return model.predict([[cgpa, experience]])[0]

# HTML Template
template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Salary Predictor</title>
</head>
<body style="
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
">
    <div style="
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        max-width: 500px;
        width: 100%;
        border: 1px solid rgba(255, 255, 255, 0.2);
    ">
        <h2 style="
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.2em;
            font-weight: 700;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">💰 Salary Predictor</h2>
        
        <form method="POST" style="display: flex; flex-direction: column; gap: 25px;">
            <div style="display: flex; flex-direction: column;">
                <label style="
                    font-weight: 600;
                    color: #555;
                    margin-bottom: 8px;
                    font-size: 1.1em;
                ">👤 Full Name</label>
                <input type="text" name="name" required style="
                    padding: 15px;
                    border: 2px solid #e1e5e9;
                    border-radius: 12px;
                    font-size: 16px;
                    transition: all 0.3s ease;
                    background: #f8f9fa;
                    outline: none;
                " 
                onfocus="this.style.borderColor='#667eea'; this.style.boxShadow='0 0 0 3px rgba(102, 126, 234, 0.1)'; this.style.background='#fff';"
                onblur="this.style.borderColor='#e1e5e9'; this.style.boxShadow='none'; this.style.background='#f8f9fa';"
                placeholder="Enter your full name">
            </div>

            <div style="display: flex; flex-direction: column;">
                <label style="
                    font-weight: 600;
                    color: #555;
                    margin-bottom: 8px;
                    font-size: 1.1em;
                ">📊 CGPA (0.0 - 10.0)</label>
                <input type="number" step="0.01" min="0" max="10" name="cgpa" required style="
                    padding: 15px;
                    border: 2px solid #e1e5e9;
                    border-radius: 12px;
                    font-size: 16px;
                    transition: all 0.3s ease;
                    background: #f8f9fa;
                    outline: none;
                "
                onfocus="this.style.borderColor='#667eea'; this.style.boxShadow='0 0 0 3px rgba(102, 126, 234, 0.1)'; this.style.background='#fff';"
                onblur="this.style.borderColor='#e1e5e9'; this.style.boxShadow='none'; this.style.background='#f8f9fa';"
                placeholder="e.g., 8.5">
            </div>

            <div style="display: flex; flex-direction: column;">
                <label style="
                    font-weight: 600;
                    color: #555;
                    margin-bottom: 8px;
                    font-size: 1.1em;
                ">💼 Experience (years)</label>
                <input type="number" step="0.1" min="0" name="experience" required style="
                    padding: 15px;
                    border: 2px solid #e1e5e9;
                    border-radius: 12px;
                    font-size: 16px;
                    transition: all 0.3s ease;
                    background: #f8f9fa;
                    outline: none;
                "
                onfocus="this.style.borderColor='#667eea'; this.style.boxShadow='0 0 0 3px rgba(102, 126, 234, 0.1)'; this.style.background='#fff';"
                onblur="this.style.borderColor='#e1e5e9'; this.style.boxShadow='none'; this.style.background='#f8f9fa';"
                placeholder="e.g., 2.5">
            </div>

            <button type="submit" style="
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 18px 30px;
                border: none;
                border-radius: 12px;
                font-size: 1.2em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 8px 15px rgba(102, 126, 234, 0.3);
                margin-top: 10px;
            "
            onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 12px 20px rgba(102, 126, 234, 0.4)';"
            onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 15px rgba(102, 126, 234, 0.3)';"
            onmousedown="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 8px rgba(102, 126, 234, 0.3)';"
            onmouseup="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 12px 20px rgba(102, 126, 234, 0.4)';">
                🚀 Predict My Salary
            </button>
        </form>

        <!-- Result section (Flask template syntax preserved) -->
        {% if salary %}
        <div style="
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
            animation: slideIn 0.5s ease-out;
        ">
            <h3 style="
                color: white;
                margin: 0;
                font-size: 1.8em;
                font-weight: 700;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            ">💸 Predicted Salary</h3>
            <p style="
                color: #f0f8ff;
                font-size: 2.5em;
                font-weight: 800;
                margin: 15px 0 0 0;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            ">₹{{ salary | round(2) }}</p>
        </div>
        {% endif %}
    </div>

    <style>
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Responsive design */
        @media (max-width: 600px) {
            body {
                padding: 10px;
            }
            
            div[style*="max-width: 500px"] {
                padding: 25px;
            }
            
            h2 {
                font-size: 1.8em !important;
            }
        }
        
        /* Add subtle animations */
        input:focus {
            animation: focusGlow 0.3s ease-in-out;
        }
        
        @keyframes focusGlow {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
    </style>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    salary = None
    if request.method == 'POST':
        name = request.form['name']
        cgpa = float(request.form['cgpa'])
        experience = float(request.form['experience'])

        salary = float(predict_salary(cgpa, experience))

        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_data (name, cgpa, experience, salary) VALUES (%s, %s, %s, %s)",
                       (name, cgpa, experience, salary))
        conn.commit()
        conn.close()

    return render_template_string(template, salary=salary)

if __name__ == '__main__':
    app.run(debug=True)
