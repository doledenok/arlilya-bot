"""Info about exam."""

import os
import enum
import csv
import random
import yaml
from typing import List, Dict


class ExamStatus(enum.Enum):
    """Current exam status."""

    Created = 0
    RegistrationFinished = 1
    PresentationsFinished = 2
    ResultsReviewFinished = 3


class Exam:
    """Info about current exam."""
    translater = {
            "stutter_count": "Количество запинок",
            "calmness_story": "Спокойствие на рассказе",
            "calmness_questions": "Спокойствие на вопросах",
            "eye_contact_story": "Зрительный контакт на рассказе",
            "eye_contact_quesitons": "Зрительный контакт на вопросах",
            "answer_skill": "Умение отвечать на вопросы",
            "notes": "Замечания",
        }
    # TODO: Сделать критерии отдельным классом, и обращаться к id критерия, а не к текстовому представлению.
    def __init__(self, name: str):
        """Create exam with id."""
        self.id = 711 #random.randrange(100, 1000)
        self.name = name
        self.speaker_names: List[str] = []
        self.speaker_answers: List[Dict[int, dict]] = []
        self.exam_status: ExamStatus = ExamStatus.Created
        self.backup_file = open(os.path.join(os.environ.get("TELEGRAM_ARLILYA_BOT_DATA", os.getcwd()), "exam_backup.yaml"), "a")

    def add_speaker(self, name: str) -> int | None:
        """Return participant id or None if name is not unique."""
        if name in self.speaker_names:
            return None
        self.speaker_names.append(name)
        self.speaker_answers.append({})
        return len(self.speaker_names) - 1

    def get_speaker_names(self, speaker_id: int = None) -> list:
        """If speaker_id is not None return all speaker names except speaker with that id."""
        if speaker_id is None:
            return self.speaker_names
        without_one_speakers = self.speaker_names[:speaker_id]
        if speaker_id >= len(self.speaker_names) - 1:
            return without_one_speakers
        return without_one_speakers + self.speaker_names[speaker_id + 1:]

    def get_name_by_id(self, speaker_id: int) -> str:
        """Return name of speaker by its id."""
        return self.speaker_names[speaker_id]  # если вдруг слишком большой id - пусть падает

    def check_rate(self, listener_id: int, speaker_id: int, criteria: str) -> bool:
        # TODO: переделать критерии в отдельный класс, и обращаться по индексу.
        if speaker_id not in self.speaker_answers[listener_id]:
            return False
        if self.translater[criteria] not in self.speaker_answers[listener_id][speaker_id]:
            return False
        return True

    def add_answer(self, listener_id: int, speaker_id: int, field: str, value: int | str):
        """
        Store score of some criteria for listener and speaker.

        Criteria are:
        - stutter_count
        - calmness_story
        - calmness_questions
        - eye_contact_story
        - eye_contact_quesitons
        - answer_skill
        - notes
        """
        if speaker_id not in self.speaker_answers[listener_id]:
            self.speaker_answers[listener_id][speaker_id] = {}
        self.speaker_answers[listener_id][speaker_id][self.translater[field]] = value
        self.make_backup()

    def make_backup(self):
        #yaml.dump(self.backup_file)
        pass

    def save_results(self, exams_csv_db: str) -> None:
        """Save all result of exam in csv file."""
        saved_rows = 0
        with open(exams_csv_db, 'a+', newline='') as csvfile:
            fieldnames = ['exam_id', 'answering_student_id', 'listening_student_id', 'question_id', 'student_mark']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if os.path.getsize(exams_csv_db) == 0:
                writer.writeheader()
            for listener_id in range(len(self.speaker_answers)):
                for speaker_id in self.speaker_answers[listener_id]:
                    for field in self.speaker_answers[listener_id][speaker_id]:
                        writer.writerow(
                            {
                                'exam_id': self.id,
                                'answering_student_id': speaker_id,
                                'listening_student_id': listener_id,
                                'question_id': field,
                                'student_mark': self.speaker_answers[listener_id][speaker_id][field],
                            }
                        )
                        saved_rows += 1
        return saved_rows
