import sys
import os

from io import StringIO
import numpy as np
import pandas as pd


sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "src")))

import exam_statistics


def test_python3():
    assert sys.version_info >= (3, 4)


def test_calculate_individual_stats():
    input_csv_file = StringIO(
        "exam_id,answering_student_id,listening_student_id,question_id,"
        "student_mark\n0,1,0,a,5\n0,2,1,b,4\n0,2,1,a,3\n0,0,1,b,6\n0,2,3,z,9\n"
    )
    output_csv_file = StringIO(
        "question_id,mean_student_mark,median_student_mark,std_student_mark,"
        "cnt_student_mark\na,4.0,4.0,1.4142,2\nb,5.0,5.0,1.4142,2\nz,9.0,9.0,,1\n"
    )
    df = pd.read_csv(input_csv_file)
    func_result = exam_statistics.calculate_individual_stats(df)

    assert np.allclose(
        func_result.fillna(-100).values, pd.read_csv(output_csv_file).set_index('question_id').fillna(-100).values
    )
