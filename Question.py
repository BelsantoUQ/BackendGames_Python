# Clase que representa la tabla QUESTIONS
class Question:
    def __init__(self, queid, que1='GAMEPLAY EXPERIENCE', que1ans=0, que2='UI AND HUD EXPERIENCE', que2ans=0, que3='VISUAL EFFECTS EXPERIENCE', que3ans=0):
        self.queid = queid
        self.que1 = que1
        self.que1ans = que1ans
        self.que2 = que2
        self.que2ans = que2ans
        self.que3 = que3
        self.que3ans = que3ans

    def __str__(self):
        return f"Question(queid={self.queid}, que1='{self.que1}', que1ans={self.que1ans}, que2='{self.que2}', que2ans={self.que2ans}, que3='{self.que3}', que3ans={self.que3ans})"
