from flask import Flask, request, render_template
from pick_tdna_primers import run_tdna_primers
from classes import primer_results
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    stock_num = ''
    if request.method == 'POST':
        stock_num = request.form['stock-num']

        a = run_tdna_primers(stock_num)
        b = primer_results(a[0]['name'],a[0]['Primers']['LP']['Sequence'], a[0]['Primers']['RP']['Sequence'], a[0]['Sequence'])
        print(b.pretty_print())
        return render_template('results.html', stock_num=stock_num, results=b.pretty_print())
    else:
        return render_template('main.html')



if __name__ == '__main__':
    app.run()
