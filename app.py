from flask import Flask , render_template , redirect , request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///bills.db"
# app.config['SQLALCHEMY_BINDS'] = {
#     "qustions" : "sqlite:///Qustions.db"
# }
db = SQLAlchemy(app)
app.app_context().push()

class Bills(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    BillID = db.Column(db.String(200) , nullable = False)
    IssueDate = db.Column(db.DateTime , nullable = False)
    LastDate = db.Column(db.DateTime , nullable = False)
    Amount = db.Column(db.Integer , nullable = False)
    Status = db.Column(db.String(200) , nullable = False)


    def __repr__(self) -> str:
        return f"{self.BillID} - {self.IssueDate} - {self.LastDate}"

@app.route("/home")
@app.route("/" , methods=['GET' , 'POST'])
def HomePage():
    if request.method == 'POST':
        billno = request.form['billno']
        bill = Bills.query.filter(BillID=billno)
        return render_template('index.html', allbills=bill)    
    allbills = Bills.query.all()[:4]
    return render_template('index.html', allbills=allbills)

@app.route("/manage")
def manage():
    allbills = Bills.query.all()
    return render_template('manage.html' , allbills=allbills)

@app.route("/add" , methods=['GET' , 'POST'])
def add():
    if request.method == 'POST':
        billno = request.form['billno']
        amt = request.form['amt']
        idate = datetime.strptime(request.form['idate'], '%Y-%m-%d')
        ldate = datetime.strptime(request.form['ldate'], '%Y-%m-%d')
        status = request.form['status']
        bill = Bills(BillID=billno , IssueDate=idate , LastDate=ldate , Status=status , Amount=amt)
        db.session.add(bill)
        db.session.commit()
        return redirect('/add')
    return render_template('addbill.html')

@app.route('/Delete/<int:BillID>')
def delete(BillID):
    quiz = Bills.query.filter_by(BillID = BillID).first()
    db.session.delete(quiz)
    db.session.commit()
    allbills = Bills.query.all()
    # return render_template('manage.html' , allbills=allbills)
    return redirect('/manage')

@app.route('/Update/<int:BillID>' , methods=['GET' , 'POST'])
def update(BillID):
    bill = Bills.query.filter_by(BillID=BillID).first()
    if request.method == 'POST':
        billno = request.form['billno']
        amt = request.form['amt']
        idate = datetime.strptime(request.form['idate'], '%Y-%m-%d')
        ldate = datetime.strptime(request.form['ldate'], '%Y-%m-%d')
        status = request.form['status']
        bill.BillID = billno
        bill.Amount = amt
        bill.IssueDate = idate
        bill.LastDate = ldate
        bill.Status = status
        db.session.commit()
        return redirect('/manage')
    
    return render_template('update.html' , bill=bill)
    

if __name__ == "__main__":
    app.run(debug=True , port=8000)