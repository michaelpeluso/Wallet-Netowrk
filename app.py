import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from db import execute_query, fetch_query
import re
from decimal import Decimal


# load env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default")

# regex patterns
ssn_pattern = re.compile(r'^\d{9}$') # matches social security numbers '123456789'
email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$') # 'user@example.com'
phone_pattern = re.compile(r'^\d{10}$') # '1234567890'
name_pattern = re.compile(r'^[A-Za-z\s]+$') # 2 words
bankid_pattern = re.compile(r'^\d+$') # any number
banum_pattern = re.compile(r'^[A-Za-z0-9]*$') # alpha-numeric characters '1234567890', 'A14gif5'
amount_pattern = re.compile(r'^\d+(\.\d{1,2})?$') # '10', '100.00', '0.99'

@app.route('/')
def index():
    # show home page
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    # user provides ssn, name, email, phone
    if request.method == 'POST':
        ssn = request.form.get('ssn', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

        # validate ssn
        if not ssn_pattern.match(ssn):
            flash('Invalid SSN format.', 'danger')
            return redirect(url_for('signup'))
        
        # validate name
        if not name or not name_pattern.match(name):
            flash('Invalid full name.', 'danger')
            return redirect(url_for('signup'))
        
        # validate email
        if not email_pattern.match(email):
            flash('Invalid email address.', 'danger')
            return redirect(url_for('signup'))
        
        # validate phone
        phone_digits = re.sub(r'\D', '', phone)  # remove non-digit characters
        if not phone_pattern.match(phone_digits):
            flash('Invalid phone number.', 'danger')
            return redirect(url_for('signup'))
        
        # interact with database
        try: 
            # check if SSN already exists
            existing_ssn = fetch_query("select * from WALLET_ACCOUNT where SSN=%s", (ssn,))
            if existing_ssn:
                flash('SSN already in use.', 'danger')
                return redirect(url_for('signup'))
            
            # check if email already exists
            existing_email = fetch_query("select * from EMAIL_ADDRESS where EmailAdd=%s", (email,))
            if existing_email:
                flash('Email already in use.', 'danger')
                return redirect(url_for('signup'))
            
            # check if phone already exists
            existing_phone = fetch_query("select * from WALLET_ACCOUNT where PhoneNo=%s", (phone_digits,))
            if existing_phone:
                flash('Phone number already in use.', 'danger')
                return redirect(url_for('signup'))
        
            # insert elec_address for phone and email if not exists
            ea_phone = fetch_query("select * from ELEC_ADDRESS where Identifier=%s", (phone_digits,))
            if not ea_phone:
                execute_query("insert into ELEC_ADDRESS (Identifier, Verified, Type) values (%s, %s, %s)",
                              (phone_digits, False, 'Phone'))
            
            ea_email = fetch_query("select * from ELEC_ADDRESS where Identifier=%s", (email,))
            if not ea_email:
                execute_query("insert into ELEC_ADDRESS (Identifier, Verified, Type) values (%s, %s, %s)",
                              (email, False, 'Email'))
            
            # insert wallet_account
            execute_query("""insert into WALLET_ACCOUNT (SSN, Name, PhoneNo, Balance, BankID, BANumber, BAVerified) 
                            values (%s, %s, %s, %s, %s, %s, %s)""", 
                        (ssn, name, phone_digits, Decimal('0.00'), None, None, False))
        
            # insert email_address
            execute_query("insert into EMAIL_ADDRESS (EmailAdd, SSN, Verified) values (%s, %s, %s)", (email, ssn, False))
            flash('Signup successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e), "danger")
    
    return render_template('signup.html') 

@app.route('/login', methods=['GET','POST'])
def login():
    # login with ssn only
    if request.method == 'POST':
        ssn = request.form.get('ssn', '').strip()
        
        # validate ssn
        if not ssn_pattern.match(ssn):
            flash('Invalid ssn format.', 'danger')
            return redirect(url_for('login'))
        
        # interact with database
        try: 
            user = fetch_query("select * from WALLET_ACCOUNT where SSN=%s", (ssn,))
            if user:
                session['ssn'] = ssn
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('invalid ssn', 'danger')
        except Exception as e:
            flash(str(e), "danger")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # show user info and transactions
    if 'ssn' not in session:
        flash('Login required.', 'warning')
        return redirect(url_for('login'))
    
    # interact with database
    try:
        ssn = session['ssn']
        user = fetch_query("select * from WALLET_ACCOUNT where SSN=%s", (ssn,))
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('logout'))
        user = user[0]
        send_txn = fetch_query("select * from SEND_TRANSACTION where SSN=%s", (ssn,))
        req_txn = fetch_query("select * from REQUEST_TRANSACTION where SSN=%s", (ssn,))
        return render_template('dashboard.html', user=user, send_transactions=send_txn, request_transactions=req_txn)
    
    except Exception as e:
        flash(str(e), "danger")

@app.route('/link_bank', methods=['GET','POST'])
def link_bank():
    # link a bank account
    if 'ssn' not in session:
        flash('Login required.', 'warning')
        return redirect(url_for('login'))
    if request.method=='POST':
        ssn = session['ssn']
        bankid = request.form.get('bankid', '').strip()
        banum = request.form.get('banum', '').strip()
        
        # validate bankid
        if not bankid_pattern.match(bankid):
            flash('Invalid bank ID.', 'danger')
            return redirect(url_for('link_bank'))
        
        # validate banum
        if not banum_pattern.match(banum):
            flash('Invalid bank account number.', 'danger')
            return redirect(url_for('link_bank'))
        
        # interact with database
        try:
            # check if bank_account exists
            ba = fetch_query("select * from BANK_ACCOUNT where BankID=%s and BANumber=%s", (bankid, banum))
            if not ba:
                execute_query("insert into BANK_ACCOUNT (BankID, BANumber, Verified) values (%s, %s, %s)",
                            (bankid, banum, False))
            
            # update wallet_account
            execute_query("update WALLET_ACCOUNT set BankID=%s, BANumber=%s, BAVerified=%s where SSN=%s",
                        (bankid, banum, False, ssn))
            flash('Bank linked.', 'success')
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            flash(str(e), "danger")

    return render_template('link_bank.html')

@app.route('/unlink_bank', methods=['POST'])
def unlink_bank():
    # unlink bank account
    if 'ssn' not in session:
        flash('Login required.', 'warning')
        return redirect(url_for('login'))
    ssn = session['ssn']
    # reset
    try: 
        execute_query("update WALLET_ACCOUNT set BankID=NULL, BANumber=NULL, BAVerified=false where SSN=%s", (ssn,))
        flash('Bank unlinked.', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(str(e), "danger")

@app.route('/send_money', methods=['GET','POST'])
def send_money():
    # send money to an email/phone
    if 'ssn' not in session:
        flash('Login required.', 'warning')
        return redirect(url_for('login'))
    if request.method=='POST':
        ssn = session['ssn']
        identifier = request.form.get('identifier', '').strip()
        amount = request.form.get('amount', '').strip()
        memo = request.form.get('memo', '').strip()
        
        # validate identifier (email or phone)
        is_email = email_pattern.match(identifier)
        is_phone = phone_pattern.match(re.sub(r'\D', '', identifier))
        if not (is_email or is_phone):
            flash('Invalid recipient identifier.', 'danger')
            return redirect(url_for('send_money'))
        if is_phone:
            identifier = re.sub(r'\D', '', identifier)  # keep digits only
        
        # validate amount
        if not amount_pattern.match(amount):
            flash('Invalid amount format.', 'danger')
            return redirect(url_for('send_money'))
        amount = float(amount)
        if amount <= 0:
            flash('Amount must be positive.', 'danger')
            return redirect(url_for('send_money'))
        
        # interact with database
        try:
            # check balance
            bal = fetch_query("select Balance from WALLET_ACCOUNT where SSN=%s", (ssn,))
            if not bal or bal[0]['Balance'] < amount:
                flash('Insufficient funds.', 'danger')
                return redirect(url_for('send_money'))
            
            # check if recipient exists
            recipient = fetch_query("select * from WALLET_ACCOUNT where SSN=(select SSN from EMAIL_ADDRESS where EmailAdd=%s) or PhoneNo=%s", (identifier, identifier))
            if not recipient:
                flash('recipient not found or not verified', 'danger')
                return redirect(url_for('send_money'))
            
            # deduct balance
            execute_query("update WALLET_ACCOUNT set Balance=Balance-%s where SSN=%s", (amount, ssn))
            
            # insert send_transaction
            execute_query("""insert into SEND_TRANSACTION (Identifier, L_DTime, C_DTime, Memo, CReason, CType, Amount, SSN)
                            values (%s, now(), now(), %s, null, 'Completed', %s, %s)""", 
                        (identifier, memo, amount, ssn))
            flash('money sent', 'success')
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            flash(str(e), "danger")

    return render_template('send_money.html')

@app.route('/request_money', methods=['GET','POST'])
def request_money():
    # request money from others
    if 'ssn' not in session:
        flash('login required', 'warning')
        return redirect(url_for('login'))
    if request.method=='POST':
        ssn = session['ssn']
        amount = request.form.get('amount', '').strip()
        memo = request.form.get('memo', '').strip()
        
        # validate amount
        if not amount_pattern.match(amount):
            flash('invalid amount format', 'danger')
            return redirect(url_for('request_money'))
        amount = float(amount)
        if amount <= 0:
            flash('amount must be positive', 'danger')
            return redirect(url_for('request_money'))
        
        try:
            # insert request_transaction
            execute_query("insert into REQUEST_TRANSACTION (Amount, DateTime, Memo, SSN) values (%s, now(), %s, %s)",
                        (amount, memo, ssn))
            flash('request created', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(str(e), "danger")

    return render_template('request_money.html')

@app.route('/manage_funds', methods=['GET', 'POST'])
def manage_funds():
    # add or subtract funds from user's account
    if 'ssn' not in session:
        flash('login required', 'warning')
        return redirect(url_for('login'))
    
    ssn = session['ssn']
    if request.method == 'POST':
        amount = request.form.get('amount', '').strip()
        action = request.form.get('action', '').strip()

        # validate amount
        if not amount_pattern.match(amount):
            flash('invalid amount format', 'danger')
            return redirect(url_for('manage_funds'))
        amount = float(amount)
        if amount <= 0:
            flash('amount must be positive', 'danger')
            return redirect(url_for('manage_funds'))

        # fetch current balance
        user = fetch_query("select Balance from WALLET_ACCOUNT where SSN=%s", (ssn,))
        if not user:
            flash('user not found', 'danger')
            return redirect(url_for('dashboard'))
        current_balance = user[0]['Balance']

        # convert amount to decimal
        from decimal import Decimal
        amount_decimal = Decimal(str(amount))  # safely convert float to decimal

        try:
            # handle add or subtract
            if action == 'add':
                new_balance = current_balance + amount_decimal
                execute_query("update WALLET_ACCOUNT set Balance=%s where SSN=%s", (new_balance, ssn))
                flash(f'${amount:.2f} added to your account', 'success')
            elif action == 'subtract':
                if amount_decimal > current_balance:
                    flash('insufficient funds', 'danger')
                else:
                    new_balance = current_balance - amount_decimal
                    execute_query("update WALLET_ACCOUNT set Balance=%s where SSN=%s", (new_balance, ssn))
                    flash(f'${amount:.2f} subtracted from your account', 'success')
            else:
                flash('invalid action', 'danger')
            
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            flash(str(e), "danger")

    # show current balance
    try:
        user = fetch_query("select Balance from WALLET_ACCOUNT where SSN=%s", (ssn,))
        balance = user[0]['Balance'] if user else 0.00
        return render_template('manage_funds.html', balance=balance)
    except Exception as e:
        flash(str(e), "danger")

@app.route('/logout')
def logout():
    # logout user
    session.pop('ssn', None)
    flash('logged out', 'success')
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)