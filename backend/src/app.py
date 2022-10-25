
from flask import Flask, request,jsonify
from flask_cors import CORS
import models as m
from connector import Connector
from sqlalchemy import select
from config import Config
import pandas as pd
import numpy as np
import json


app = Flask(__name__)
CORS(app)


m.create_all_models()
db = Connector(Config.DB_ENDPOINT)
sess = db.db_session

def find_user_by_username(user: str):
    # user = sess.execute(
    #     select(m.User).where(m.User.username == user)
    # ).first()
    user = sess.query(m.User).where(m.User.username == user).one()
    return user

def find_user_by_id(user: str):
    # user = sess.execute(
    #     select(m.User).where(m.User.username == user)
    # ).first()
    user = sess.query(m.User).where(m.User.id == id).one()
    return user

def find_group_by_name(name: str):
    group = sess.query(m.Group).where(m.Group.group_name == name).one()
    return group

def find_user_group_by_user_and_group(user_id, group_id):
    user_group  = sess.query(m.UserGroup).where(m.UserGroup.user_id == user_id and m.UserGroup.group_id==group_id).one()
    return user_group

def find_user_group_by_id(usergroup_id):
    user_group  = sess.query(m.UserGroup).where(m.UserGroup.id == usergroup_id).one()
    return user_group

@app.route("/")
def root():
    return 'Service is working', 200


@app.route('/user',methods=['POST'])
def create_user():
    data = request.get_json()
    for dat in data:
        user = m.User(username=dat['username'], email=dat['email'])
        sess.add(user)
        sess.commit()
    return 'Created', 201


@app.route('/group', methods=['POST'])
def create_group():
    data = request.get_json()
    creator = find_user_by_username(data['created_by'])
    group = m.Group(group_name = data['group_name'],created_by=creator.id)
    sess.add(group)
    sess.commit()

    userg = m.UserGroup(user_id=creator.id,group_id=group.id)
    sess.add(userg)
    sess.commit()

    for dat in data['members']:
        member = find_user_by_username(dat)
        userg = m.UserGroup(user_id=member.id,group_id=group.id)
        sess.add(userg)
        sess.commit()


    return 'Created', 201


@app.route('/expense', methods=['POST'])
def create_expense():
    data = request.get_json()
    payer = find_user_by_username(data['payer'])
    group = find_group_by_name(data['group_name'])
    # user_group = find_user_group_by_user_and_group(payer.id,group.id)

    expense = m.Expense(expense_name=data['expense_name'],amount=data['total_paid'],group_id = group.id)
    sess.add(expense)
    sess.commit()

    users = [payer]
    shares = data['shares']

    for dat in data['payees']:
            member = find_user_by_username(dat)
            users.append(member)


    pendings = [sum(shares) - shares[0]]

    for i in range(1,len(shares)):
        pendings.append(-1*shares[i])


    for i in range(len(users)):
        expense_split = m.ExpenseSplit(expense_id=expense.id,payee_id=users[i].id,share_amount=shares[i],pending_amount=pendings[i],payer_id=payer.id)
        sess.add(expense_split)
        sess.commit()

    
    return 'Created', 201


@app.route('/expense', methods=['PUT'])
def update_expense():
    # Right now this method will be used for settlement, but later on will be modified for other updates as well
    # accept:
    # group name
    # settler
    # settlee
    data = request.get_json()
    payer = find_user_by_username(data['payer'])
    payee = find_user_by_username(data['payee'])
    group = find_group_by_name(data['group_name'])



    # find:
    # settler id
    # settlee id
    # group id
    # expense id with above group id
    # filter expense_splits with expense id with above group ids
    expenses = sess.query(m.Expense).where(m.Expense.group_id==group.id).all()
    expense_ids = []
    for expense in expenses:
        expense_ids.append(expense.id)

    expense_splits = sess.query(m.ExpenseSplit).where(
        m.ExpenseSplit.expense_id.in_(tuple(expense_ids)) 
        # m.ExpenseSplit.payee_id.in_((payer.id, payee.id)) and
        # m.ExpenseSplit.payer_id.in_((payer.id, payee.id))
    ).filter(m.ExpenseSplit.payee_id.in_((payer.id, payee.id))).filter(m.ExpenseSplit.payer_id.in_((payer.id, payee.id)))

    # rows = []
    # for row in expense_splits:
    #     rows.append(dict(row))
    # filter all rows with settler and settle

    df = pd.read_sql(expense_splits.statement, expense_splits.session.bind)
    # df.to_csv('notebooks/test.csv',index=False)

    # SUM of shares of non-negative pendings
    shares_sum = np.sum(df[df.pending_amount >= 0].share_amount)
    negative_pendings_grouped = df[df.pending_amount < 0].groupby('payee_id').sum()['pending_amount'].reset_index()
    pendings = np.abs(negative_pendings_grouped.pending_amount.values)
    is_first_payer = None
    if pendings[0] < pendings[1]:
        is_first_payer = False
    else:
        is_first_payer = True
    is_first_payer

    receiver_id = None
    payer_id = None
    if is_first_payer:
        payer_id = negative_pendings_grouped.payee_id[0]
        receiver_id = negative_pendings_grouped.payee_id[1]
    else:
        payer_id = negative_pendings_grouped.payee_id[1]
        receiver_id = negative_pendings_grouped.payee_id[0]

    amount_to_transfer = np.abs(shares_sum - np.sum(pendings))

    payer_name = None
    receiver_name = None
    if payer.id == payer_id:
        payer_name = payer.username
        receiver_name = payee.username
    else:
        payer_name = payee.username
        receiver_name = payer.username

    dat = {
        'payer': payer_name,
        'receiver': receiver_name,
        'amount':amount_to_transfer
    }
    


    return jsonify(dat),202
