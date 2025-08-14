import streamlit as st
import pandas as pd
import pickle
st.set_page_config(page_title='Loan_predictor',page_icon='loan.png')
st.header('💰Loan Eligibility Predictor')
st.subheader('Check your loan apporval chances instantly')
df=pd.read_csv('cleaned_df.csv')
objects={}
for i in df.columns:
    if df[i].dtype==object:
        objects[i]=list(df[i].unique())
        objects[i].sort()
with open('rfmodel.pkl','rb') as file:
    model=pickle.load(file)

with st.container(border=True):
    col1,col2=st.columns(2)
    gender=col1.selectbox('Person_gender:',options=objects['person_gender'])
    age=col2.number_input('Person_age:',min_value=18,max_value=90)
    education=st.selectbox('Person_education:',options=objects['person_education'])
    c1,c2=st.columns(2)
    income=c1.number_input('Person_income:',min_value=5000)
    experience=c2.number_input('Person_emp_exp:',min_value=0)
    ownership=st.selectbox('Person_home_ownership',options=objects['person_home_ownership'])
    loan_amount=st.number_input('Loan_amount:')
    loan_intent=st.selectbox('Loan_intention:',options=objects['loan_intent'])
    loan_int_rate=st.number_input('Loan_interest_rate:')
    loan_percent_income=st.number_input('Loan_percent_income:')
    cb_person_cred_hist_length=st.number_input('Credit_history:')
    credit_score=st.number_input('Credit_score:')

    previous_loan_defaults_on_file=st.radio('Is there any previous loan defaults on file',options=objects['previous_loan_defaults_on_file'],horizontal=True)
    input_values=[[age,objects['person_gender'].index(gender),objects['person_education'].index(education),income,experience,objects['person_home_ownership'].index(ownership),\
                 loan_amount,objects['loan_intent'].index(loan_intent),loan_int_rate,loan_percent_income,cb_person_cred_hist_length,credit_score,objects['previous_loan_defaults_on_file'].index(previous_loan_defaults_on_file)]]
    c1,c2,c3=st.columns([1.5,1.6,1])
    if c2.button('Submit'):
        out=model.predict(input_values)
        if out[0]==1:
            st.subheader('Loan can be sanctioned')
        else:
            st.subheader('Loan can not be sanctioned')


