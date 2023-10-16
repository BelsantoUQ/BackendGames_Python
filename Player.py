class PlayerInfo:
    def __init__(self, plyid, plyscore=0, plylife=0, plygame=1, plygames=0, plypos=None, plyrot=None, plypowerups=0, plyname=None, plyemail=None, plypass=None):
        self.plyid = plyid
        self.plyscore = plyscore
        self.plygame = plygame
        self.plylife = plylife
        self.plygames = plygames
        self.plypos = plypos
        self.plyrot = plyrot
        self.plypowerups = plypowerups
        self.plyname = plyname
        self.plyemail = plyemail
        self.plypass = plypass
        self.questions = []

    def __str__(self):
        player_info_str = f"Player ID: {self.plyid}\n"
        player_info_str += f"Player Score: {self.plyscore}\n"
        player_info_str += f"Player Game: {self.plygame}\n"
        player_info_str += f"Player Life: {self.plylife}\n"
        player_info_str += f"Player Games: {self.plygames}\n"
        player_info_str += f"Player Position: {self.plypos}\n"
        player_info_str += f"Player Rotation: {self.plyrot}\n"
        player_info_str += f"Player Powerups: {self.plypowerups}\n"
        player_info_str += f"Player Name: {self.plyname}\n"
        player_info_str += f"Player Email: {self.plyemail}\n"
        player_info_str += f"Player Password: {self.plypass}\n"

        if self.questions:
            player_info_str += "Questions:\n"
            for question in self.questions:
                player_info_str += f"Question ID: {question.queid}\n"
                player_info_str += f"Question 1: {question.que1} - Answer: {question.que1ans}\n"
                player_info_str += f"Question 2: {question.que2} - Answer: {question.que2ans}\n"
                player_info_str += f"Question 3: {question.que3} - Answer: {question.que3ans}\n"

        return player_info_str

    def get_questions(self):
        return self.questions

    def add_question(self, newQuestion):
        self.questions.append(newQuestion)

    def search_question_by_id(self, id_question):
        left, right = 0, len(self.questions) - 1
        while left <= right:
            middle = (left + right) // 2
            if self.questions[middle].queid == id_question:
                return self.questions[middle]
            elif self.questions[middle].queid < id_question:
                left = middle + 1
            else:
                right = middle - 1
        return None
