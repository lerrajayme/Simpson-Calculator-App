from flask import Flask, render_template, request
import math

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

def composite_simpson_1_3_with_steps(f, a, b, n):
    """
    Returns (result, steps_html) where steps_html contains step-by-step explanation.
    """
    if n % 2 != 0:
        raise ValueError("Number of subintervals n must be even.")
    
    h = (b - a) / n
    steps = []
    
    # Step 1
    steps.append(f"<strong>Step 1:</strong> Compute step size \( h = \\frac{{b - a}}{{n}} = \\frac{{{b} - {a}}}{{{n}}} = {h:.6f} \)")
    
    # Step 2: nodes
    x_vals = [a + i * h for i in range(n + 1)]
    steps.append(f"<strong>Step 2:</strong> Divide the interval into \( n = {n} \) subintervals of equal width. The nodes are:")
    x_list_str = ", ".join([f"\(x_{i} = {x:.4f}\)" for i, x in enumerate(x_vals)])
    steps.append(x_list_str)
    
    # Step 3: f(x_i)
    f_vals = [f(x) for x in x_vals]
    steps.append("<strong>Step 3:</strong> Evaluate \( f(x) \) at each node:")
    f_list_str = ", ".join([f"\(f(x_{i}) = {val:.6f}\)" for i, val in enumerate(f_vals)])
    steps.append(f_list_str)
    
    # Step 4: formula components
    f0_fn = f_vals[0]
    fn_fn = f_vals[-1]
    sum_odd = sum(f_vals[i] for i in range(1, n, 2))
    sum_even = sum(f_vals[i] for i in range(2, n-1, 2))
    
    steps.append("<strong>Step 4:</strong> Apply Simpson's 1/3 rule formula:")
    steps.append(r"\[ \int_a^b f(x)\,dx \approx \frac{h}{3}\left[ f(x_0) + f(x_n) + 4\sum_{\text{odd}} f(x_i) + 2\sum_{\text{even}} f(x_i) \right] \]")
    steps.append(f"Here:")
    steps.append(f"- \( f(x_0) = {f0_fn:.6f} \), \( f(x_n) = {fn_fn:.6f} \)")
    
    # Odd indices
    odd_vals = [f_vals[i] for i in range(1, n, 2)]
    odd_sum_str = " + ".join([f"{v:.6f}" for v in odd_vals])
    steps.append(f"- Sum over odd indices (1,3,5,…): \( 4 \\times ({odd_sum_str}) = 4 \\times {sum_odd:.6f} = {4*sum_odd:.6f} \)")
    
    # Even indices
    even_vals = [f_vals[i] for i in range(2, n-1, 2)]
    if even_vals:
        even_sum_str = " + ".join([f"{v:.6f}" for v in even_vals])
        steps.append(f"- Sum over even indices (2,4,… up to n-2): \( 2 \\times ({even_sum_str}) = 2 \\times {sum_even:.6f} = {2*sum_even:.6f} \)")
    else:
        steps.append(f"- Sum over even indices: (none, because n-2 < 2) → \( 2 \\times {sum_even:.6f} = {2*sum_even:.6f} \)")
    
    # Step 5: total sum
    total = f0_fn + fn_fn + 4*sum_odd + 2*sum_even
    steps.append(f"<strong>Step 5:</strong> Add all contributions:")
    steps.append(f"\[ S = {f0_fn:.6f} + {fn_fn:.6f} + {4*sum_odd:.6f} + {2*sum_even:.6f} = {total:.6f} \]")
    
    # Step 6: final multiplication
    factor = h / 3
    result = factor * total
    steps.append(f"<strong>Step 6:</strong> Multiply by \( \\frac{{h}}{{3}} = \\frac{{{h:.6f}}}{{3}} = {factor:.6f} \):")
    steps.append(f"\[ \int_a^b f(x) \, dx \\approx {factor:.6f} \\times {total:.6f} = {result:.8f} \]")
    
    # Join steps into HTML with proper line breaks and LaTeX rendering class
    steps_html = "<div class='step-by-step'>" + "".join(f"<p>{step}</p>" for step in steps) + "</div>"
    return result, steps_html

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
    steps_html = None
    if request.method == 'POST':
        try:
            func_str = request.form['function']
            a = float(request.form['a'])
            b = float(request.form['b'])
            n = int(request.form['n'])
            
            # Safe evaluation function
            def f(x_val):
                return eval(func_str, {"__builtins__": {}}, {"x": x_val, "math": math})
            
            result, steps_html = composite_simpson_1_3_with_steps(f, a, b, n)
        except Exception as e:
            error = str(e)
    
    return render_template('calculator.html', result=result, error=error, steps=steps_html)

if __name__ == '__main__':
    app.run(debug=True)