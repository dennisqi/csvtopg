import sys
import timeit
import math
import pandas as pd
import numpy as np
from collections import Counter

sys.path.insert(0, '../csvtopg/csvtopg')
from csvhelper import read_df_lines


def distribution_of_member_id_occurance(csv):
    """Count the number of occurance for each member id."""
    df = pd.read_csv(csv)
    c = Counter(line['member_id'] for line in read_df_lines(df))
    return Counter(c.values())


if __name__ == '__main__':
    csv = 'data/loan_head.csv'
    # csv = 'data/loan.csv'
    distribution = distribution_of_member_id_occurance(csv)
