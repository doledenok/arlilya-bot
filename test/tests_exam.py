import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "src")))

import exam


def test_python3():
    assert sys.version_info >= (3, 4)


def test_Exam_add_speaker():
    new_exam = exam.Exam(0)

    new_exam.add_speaker('Alina')
    assert new_exam.speaker_names == ['Alina']
    assert len(new_exam.speaker_answers) == 1

    new_exam = exam.Exam(0)
    several_names = ['Alina', 'Vasya', 'Egor', 'Vasya', 'Egor', 'Vasya', 'Nastya', 'Alina']
    for name in several_names:
        new_exam.add_speaker(name)
    assert new_exam.speaker_names == ['Alina', 'Vasya', 'Egor', 'Nastya']
    assert len(new_exam.speaker_answers) == 4


def test_Exam_get_speaker_names():
    new_exam = exam.Exam(0)
    several_names = ['Alina', 'Vasya', 'Egor', 'Vasya', 'Egor', 'Vasya', 'Nastya', 'Alina']
    for name in several_names:
        new_exam.add_speaker(name)

    assert new_exam.get_speaker_names() == ['Alina', 'Vasya', 'Egor', 'Nastya']
    assert new_exam.get_speaker_names(0) == ['Vasya', 'Egor', 'Nastya']
    assert new_exam.get_speaker_names(1) == ['Alina', 'Egor', 'Nastya']
    assert new_exam.get_speaker_names(2) == ['Alina', 'Vasya', 'Nastya']
    assert new_exam.get_speaker_names(3) == ['Alina', 'Vasya', 'Egor']


def test_Exam_get_name_by_id():
    new_exam = exam.Exam(0)
    several_names = ['Alina', 'Vasya', 'Egor', 'Vasya', 'Egor', 'Vasya', 'Nastya', 'Alina']
    for name in several_names:
        new_exam.add_speaker(name)

    names_list = ['Alina', 'Vasya', 'Egor', 'Nastya']
    assert new_exam.get_name_by_id(0) == names_list[0]
    assert new_exam.get_name_by_id(1) == names_list[1]
    assert new_exam.get_name_by_id(2) == names_list[2]
    assert new_exam.get_name_by_id(3) == names_list[3]
    assert new_exam.get_name_by_id(-1) == names_list[-1]
    assert new_exam.get_name_by_id(-2) == names_list[-2]
    assert new_exam.get_name_by_id(-3) == names_list[-3]
    assert new_exam.get_name_by_id(-4) == names_list[-4]


def test_Exam_add_answer():
    new_exam = exam.Exam(0)
    several_names = ['Alina', 'Vasya', 'Egor', 'Nastya']
    for name in several_names:
        new_exam.add_speaker(name)

    new_exam.add_answer(0, 1, 'a', 5)
    new_exam.add_answer(1, 2, 'b', 4)
    new_exam.add_answer(1, 0, 'b', 6)
    new_exam.add_answer(3, 2, 'z', 9)
    new_exam.add_answer(1, 2, 'a', 3)

    assert new_exam.speaker_answers == [{1: {'a': 5}}, {2: {'b': 4, 'a': 3}, 0: {'b': 6}}, {}, {2: {'z': 9}}]
