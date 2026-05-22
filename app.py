from flask import Flask, render_template, request
import math

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Prepare a safe namespace with all math functions
MATH_NAMESPACE = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}
# Add common aliases (optional)
MATH_NAMESPACE['pi'] = math.pi
MATH_NAMESPACE['e'] = math.e

def composite_simpson_1_3(f, a, b, n):
    """
    Composite Simpson's 1/3 rule.
    n must be even.
    """
    if n % 2 != 0:
        raise ValueError("Number of subintervals n must be even.")
    h = (b - a) / n
    integral = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            integral += 2 * f(x)
        else:
            integral += 4 * f(x)
    integral *= h / 3
    return integral

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/method')
def method():
    return render_template('method.html')

@app.route('/examples')
def examples():
    return render_template('examples.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    error = None
    if request.method == 'POST':
        try:
            func_str = request.form['function']
            a = float(request.form['a'])
            b = float(request.form['b'])
            n = int(request.form['n'])

            # Safe evaluation: only math functions and x are allowed
            def f(x_val):
                # Create a fresh namespace with x and all math functions
                namespace = MATH_NAMESPACE.copy()
                namespace['x'] = x_val
                return eval(func_str, {"__builtins__": {}}, namespace)

            result = composite_simpson_1_3(f, a, b, n)
        except Exception as e:
            error = str(e)
    return render_template('calculator.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)