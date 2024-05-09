import pandas as pd

d_work = pd.read_csv('data_csv/D_work.csv')
d_pens = pd.read_csv('data_csv/D_pens.csv')
d_clients = pd.read_csv('data_csv/D_clients.csv')
d_loan = pd.read_csv('data_csv/D_loan.csv')
d_close_loan = pd.read_csv('data_csv/D_close_loan.csv')
d_target = pd.read_csv('data_csv/D_target.csv')
d_job = pd.read_csv('data_csv/D_job.csv')
d_salary = pd.read_csv('data_csv/D_salary.csv')
d_last_credit = pd.read_csv('data_csv/D_last_credit.csv')

def gluing_tables():

    d_clients.rename(columns={'ID': 'ID_CLIENT'}, inplace=True)

    d_total = d_clients.merge(d_salary[['ID_CLIENT', 'PERSONAL_INCOME']], how='inner', on='ID_CLIENT')

    all_info_loans = d_loan.merge(d_close_loan, on='ID_LOAN', how='inner')
    series_client_loans = all_info_loans.groupby('ID_CLIENT')['ID_LOAN'].count().reset_index()
    series_client_loans.rename(columns={'ID_LOAN': 'Loan_count'}, inplace=True)
    d_total = d_total.merge(series_client_loans, on='ID_CLIENT', how='inner')

    clients_closed_loans = all_info_loans[all_info_loans['CLOSED_FL'] == 1].groupby('ID_CLIENT')['CLOSED_FL'].count().reset_index()

    d_total = d_total.merge(clients_closed_loans[['ID_CLIENT', 'CLOSED_FL']], on='ID_CLIENT', how='left')
    d_total['CLOSED_FL'] = d_total['CLOSED_FL'].fillna(.0)

    d_total = d_total.merge(d_target[['ID_CLIENT', 'TARGET']], how='left', on='ID_CLIENT')

    d_total.drop_duplicates(inplace=True)

    return d_total
