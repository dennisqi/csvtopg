from cerberus import Validator

cols = [
    'id', 'member_id', 'loan_amnt', 'funded_amnt', 'funded_amnt_inv', 'term',
    'int_rate', 'installment', 'grade', 'sub_grade', 'emp_title', 'emp_length',
    'home_ownership', 'annual_inc', 'verification_status', 'issue_d',
    'loan_status', 'pymnt_plan', 'url', 'desc', 'purpose', 'title', 'zip_code',
    'addr_state', 'dti', 'delinq_2yrs', 'earliest_cr_line', 'inq_last_6mths',
    'mths_since_last_delinq', 'mths_since_last_record', 'open_acc', 'pub_rec',
    'revol_bal', 'revol_util', 'total_acc', 'initial_list_status', 'out_prncp',
    'out_prncp_inv', 'total_pymnt', 'total_pymnt_inv', 'total_rec_prncp',
    'total_rec_int', 'total_rec_late_fee', 'recoveries',
    'collection_recovery_fee', 'last_pymnt_d', 'last_pymnt_amnt',
    'next_pymnt_d', 'last_credit_pull_d', 'collections_12_mths_ex_med',
    'mths_since_last_major_derog', 'policy_code', 'application_type',
    'annual_inc_joint', 'dti_joint', 'verification_status_joint',
    'acc_now_delinq', 'tot_coll_amt', 'tot_cur_bal', 'open_acc_6m',
    'open_il_6m', 'open_il_12m', 'open_il_24m', 'mths_since_rcnt_il',
    'total_bal_il', 'il_util', 'open_rv_12m', 'open_rv_24m', 'max_bal_bc',
    'all_util', 'total_rev_hi_lim', 'inq_fi', 'total_cu_tl', 'inq_last_12m'
]

addr_states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

application_types = ['INDIVIDUAL', 'JOINT']

grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
sub_grades = [
    'A1', 'A2', 'A3', 'A4', 'A5',
    'B1', 'B2', 'B3', 'B4', 'B5',
    'C1', 'C2', 'C3', 'C4', 'C5',
    'D1', 'D2', 'D3', 'D4', 'D5',
    'E1', 'E2', 'E3', 'E4', 'E5',
    'F1', 'F2', 'F3', 'F4', 'F5',
    'G1', 'G2', 'G3', 'G4', 'G5'
]


home_ownerships = ['RENT', 'OWN', 'MORTGAGE', 'OTHER']

initial_list_status = ['W', 'F', 'w', 'f']

policy_codes = [1, 2]

pymnt_plans = ['y', 'n']

terms = ['36 months', '60 months']

all_schema = {
    'acc_now_delinq': {'type': 'number'},
    'addr_state': {'type': 'string', 'allowed': addr_states},
    'all_util': {'type': 'number'},
    'annual_inc': {'type': 'number'},
    'annual_inc_joint': {'type': 'number'},
    'application_type': {'type': 'string', 'allowed': application_types},
    'collection_recovery_fee': {'type': 'number'},
    'collections_12_mths_ex_med': {'type': 'number'},
    'delinq_2yrs': {'type': 'number'},
    'desc': {'anyof': [{'type': 'number'}, {'type': 'string'}]},
    'dti': {'type': 'number'},
    'dti_joint': {'type': 'number'},
    'earliest_cr_line': {'type': 'string'},
    'emp_length': {'anyof': [{'type': 'number'}, {'type': 'string'}]},
    'emp_title': {'anyof': [{'type': 'number'}, {'type': 'string'}]},
    'funded_amnt': {'type': 'number'},
    'funded_amnt_inv': {'type': 'number'},
    'grade': {'type': 'string', 'allowed': grades},
    'home_ownership': {'type': 'string', 'allowed': home_ownerships},
    'id': {'type': 'number'},
    'il_util': {'type': 'number'},
    'initial_list_status': {'type': 'string', 'allowed': initial_list_status},
    'inq_fi': {'type': 'number'},
    'inq_last_12m': {'type': 'number'},
    'inq_last_6mths': {'type': 'number'},
    'installment': {'type': 'number'},
    'int_rate': {'type': 'number'},
    'issue_d': {'type': 'string'},
    'last_credit_pull_d': {'type': 'string'},
    'last_pymnt_amnt': {'type': 'number'},
    'last_pymnt_d': {'anyof': [{'type': 'number'}, {'type': 'string'}]},
    'loan_amnt': {'type': 'number'},
    'loan_status': {'type': 'string'},
    'max_bal_bc': {'type': 'number'},
    'member_id': {'type': 'number'},
    'mths_since_last_delinq': {'type': 'number', 'nullable': True},
    'mths_since_last_major_derog': {'type': 'number', 'nullable': True},
    'mths_since_last_record': {'type': 'number', 'nullable': True},
    'mths_since_rcnt_il': {'type': 'number', 'nullable': True},
    'next_pymnt_d': {'anyof': [{'type': 'number'}, {'type': 'string'}]},
    'open_acc': {'type': 'number', 'nullable': True},
    'open_acc_6m': {'type': 'number', 'nullable': True},
    'open_il_12m': {'type': 'number', 'nullable': True},
    'open_il_24m': {'type': 'number', 'nullable': True},
    'open_il_6m': {'type': 'number', 'nullable': True},
    'open_rv_12m': {'type': 'number', 'nullable': True},
    'open_rv_24m': {'type': 'number', 'nullable': True},
    'out_prncp': {'type': 'number'},
    'out_prncp_inv': {'type': 'number'},
    'policy_code': {'type': 'number', 'allowed': policy_codes},
    'pub_rec': {'type': 'number'},
    'purpose': {'type': 'string'},
    'pymnt_plan': {'type': 'string', 'allowed': pymnt_plans},
    'recoveries': {'type': 'number'},
    'revol_bal': {'type': 'number'},
    'revol_util': {'type': 'number'},
    'sub_grade': {'type': 'string', 'allowed': sub_grades},
    'term': {'type': 'string'},
    'title': {'type': 'string'},
    'tot_coll_amt': {'type': 'number', 'nullable': True},
    'tot_cur_bal': {'type': 'number', 'nullable': True},
    'total_acc': {'type': 'number'},
    'total_bal_il': {'type': 'number', 'nullable': True},
    'total_cu_tl': {'type': 'number', 'nullable': True},
    'total_pymnt': {'type': 'number'},
    'total_pymnt_inv': {'type': 'number'},
    'total_rec_int': {'type': 'number'},
    'total_rec_late_fee': {'type': 'number'},
    'total_rec_prncp': {'type': 'number'},
    'total_rev_hi_lim': {'type': 'number', 'nullable': True},
    'url': {'type': 'string'},
    'verification_status': {'type': 'string'},
    'verification_status_joint': {'anyof': [{'type': 'number'}, {'type': 'string'}]},
    'zip_code': {'type': 'string'}
}

all_validator = Validator(all_schema)

validators = {
    'all': all_validator
}
