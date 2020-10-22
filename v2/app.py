from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
from io import BytesIO
import base64
import seaborn as sns

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('base.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/poisson')
def poisson():
   return render_template('poisson.html')

@app.route('/poisson_plot',methods = ['POST', 'GET'])
def poisson_sim():
    np.random.seed(101)
    img=BytesIO()
    lambda_po=float(request.form['Poisson Parameter'])
    no_of_sim=int(request.form['Number of Simulations'])
    s = np.random.poisson(lambda_po,no_of_sim)
    sns.set_style("white")
    sns.countplot(s)
    plt.title(f"Poisson Distribution with parameter (\u03BB = {lambda_po:.2f})")
    plt.xlabel("Number of Instances per each simulation")
    plt.ylabel("Tally")
    plt.savefig(img,format='png')
    plt.close()
    img.seek(0)
    plot_url=base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('poisson_plot.html', plot_url=plot_url)

@app.route('/lognormal')
def lognormal():
   return render_template('lognormal.html')

@app.route('/lognormal_plot',methods = ['POST', 'GET'])
def lognormal_sim():
    np.random.seed(101)
    img=BytesIO()
    no_of_sim=int(request.form['Number of Simulations'])
    median=float(request.form['Median'])
    mu=np.log(median)
    sigma=float(request.form['Volatility'])
    s = np.random.lognormal(mu,sigma,no_of_sim)
    count, bins, ignored = plt.hist(s,100,density=True,align='mid')
    x = np.linspace(min(bins), max(bins), 10000)
    pdf = (np.exp(-(np.log(x)-mu)**2/(2*sigma**2))/(x*sigma*np.sqrt(2*np.pi)))
    plt.plot(x,pdf,linewidth=2,color='r')
    plt.axis('tight')
    plt.xlabel('Magnitude of an instance')
    plt.ylabel("Probability Density Function")
    plt.title(f"Log-Normal(\u03BC={mu:.2}, \u03C3={sigma:.2})")
    plt.savefig(img,format='png')
    plt.close()
    img.seek(0)
    plot_url=base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('lognormal_plot.html', plot_url=plot_url)


if __name__ == '__main__':
   app.run()
