from flask import Flask, request, render_template
from pick_tdna_primers import run_tdna_primers
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    stock_num = ''
    if request.method == 'POST':
        stock_num = request.form['stock-num']

        a = run_tdna_primers(stock_num)
        print(a)
        return render_template('results.html', stock_num=stock_num, results=a)
    else:
        return render_template('main.html')



if __name__ == '__main__':
    app.run()
