import mysql.connector
from Player import PlayerInfo
from Question import Question

class DataStore:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # Conectar a la base de datos (ajusta los parámetros según tu configuración)
        self.connection = mysql.connector.connect(
            host='containers-us-west-116.railway.app',
            port='5932',
            user='root',
            password='QWNT7GXJiTnfWAhc750E',
            db='railway',
            charset='utf8mb4'
        )
        print("DB connected")
        self.games_list = {}

    def load_players(self):
        cursor = self.connection.cursor()
        games_query = "SELECT PLYGAME, COUNT(PLYID) FROM PLAYERINFO GROUP BY PLYGAME"
        try:
            cursor.execute(games_query)
            games_db = cursor.fetchall()
            self.games_list = [[] for _ in range(len(games_db))]
            for game in games_db:
                gameId, dataAmount = game
                query = "SELECT PLYID, PLYSCORE, PLYGAME, PLYLIFE, PLYGAMES, PLYPOS, PLYROT, PLYPOWERUPS, PLYNAME, PLYEMAIL FROM PLAYERINFO WHERE PLYGAME = %s"
                params = (gameId,)
                cursor.execute(query, params)
                players_db = cursor.fetchall()
                players_list = []
                self.games_list[gameId] = players_list
                for player_db in players_db:
                    if gameId - 1 < len(self.games_list):
                        plyid, plyscore, plygame, plylife, plygames, plypos, plyrot, plypowerups, plyname, plyemail = player_db
                        query = "SELECT QUEID, QUE1ANS, QUE2ANS, QUE3ANS FROM QUESTIONS WHERE QUEPYRID = %s"
                        params = (plyid,)
                        cursor.execute(query, params)
                        questions_db = cursor.fetchall()
                        player = PlayerInfo(plyid=plyid, plyscore=plyscore, plygame=plygame, plylife=plylife, plygames=plygames, plypos=plypos, plyrot=plyrot, plypowerups=plypowerups, plyname=plyname, plyemail=plyemail)
                        for question_db in questions_db:
                            queid, que1ans, que2ans, que3ans = question_db
                            question = Question(queid=queid, que1ans=que1ans, que2ans=que2ans, que3ans=que3ans)
                            player.questions.append(question)
                        self.add_player(player, gameId)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def insert_player(self, player):
        if self.find_player_by_email_and_game(player.plyemail, player.plygame) is None or player.plyemail.strip().lower() == "n/a":
            query = "INSERT INTO PLAYERINFO (PLYGAME, PLYSCORE, PLYLIFE, PLYGAMES, PLYPOS, PLYROT, PLYPOWERUPS, PLYNAME, PLYEMAIL, PLYPASS, PLYCREATION, PLYCDATE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            params = (
                player.plygame,
                player.plyscore,
                player.plylife,
                player.plygames,
                player.plypos,
                player.plyrot,
                player.plypowerups,
                player.plyname,
                player.plyemail,
                player.plypass,
                player.plycreation,
                player.plycdate,
            )
            self.execute_query(query, params)
            self.load_players()
            print("Player added successfully.")
            return True
        else:
            return False

    def update_player_by_id(self, player):
        query = "UPDATE PLAYERINFO SET PLYGAME=%s, PLYSCORE=%s, PLYLIFE=%s, PLYGAMES=%s, PLYPOS=%s, PLYROT=%s, PLYPOWERUPS=%s, PLYNAME=%s, PLYEMAIL=%s, PLYPASS=%s, PLYUPDATE=%s, PLYUDATE=%s WHERE PLYID=%s"
        params = (
            player.plygame,
            player.plyscore,
            player.plylife,
            player.plygames,
            player.plypos,
            player.plyrot,
            player.plypowerups,
            player.plyname,
            player.plyemail,
            player.plypass,
            player.plyupdate,
            player.plyudate,
            player.plyid,
        )
        self.execute_query(query, params)
        self.load_players()
        print("Player updated successfully.")

    def find_player_by_email_and_game(self, email, game):
        query = "SELECT PLYID, PLYSCORE, PLYGAME, PLYLIFE, PLYGAMES, PLYPOS, PLYROT, PLYPOWERUPS, PLYNAME, PLYEMAIL FROM PLAYERINFO WHERE PLYEMAIL = %s AND PLYGAME = %s"
        params = (email, game)
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            if result:
                plyid, plyscore, plygame, plylife, plygames, plypos, plyrot, plypowerups, plyname, plyemail = result
                player = PlayerInfo(plyid, plyscore, plylife, plygame, plygames, plypos, plyrot, plypowerups, plyname, plyemail)
                return player
            else:
                print("No player found with the provided email and game.")
                return None

    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.connection.commit()
        except Exception as e:
            print(f"Error en la consulta: {e}")

    def close_connection(self):
        self.connection.close()

    def add_player(self, player_info, game_key):
        self.games_list[game_key].append(player_info)

    def get_players(self, game):
        return self.games_list[game]

    def get_games(self):
        return self.games_list

    def search_player_by_id(self, id_player, game):
        left, right = 0, len(self.get_players(game)) - 1
        while left <= right:
            middle = (left + right) // 2
            if self.get_players(game)[middle].plyid == id_player:
                return self.get_players(game)[middle]
            elif self.get_players(game)[middle].plyid < id_player:
                left = middle + 1
            else:
                right = middle - 1
        return None

    def get_players_by_game(self, game):
        return self.games_list[game]

    def imprimir_lista(self):
        str_games = ""
        for element in self.games_list:
            if isinstance(element, list):
                self.imprimir_lista(element)  # Llamada recursiva para listas anidadas
            else:
                str_games += (element + "Ω")
        return str_games

# Ejemplo de uso:
# if __name__ == "__main__":
#     # Crear una instancia de la clase Singleton para la base de datos
#     db = DataStore()
#     db.loadPlayers()
#     mi_lista = db.get_games()
    # Ejecutar una consulta de ejemplo (reemplaza con tus propias consultas)
    # query = "INSERT INTO PLAYERINFO (PYRLIFE, PLYNAME, PLYEMAIL, PLYPASS) VALUES (%s, %s, %s, %s)"
    # params = (100, "ejemplo", "ejemplo@example.com", "contraseña")
    # db.execute_query(query, params)
    # Cerrar la conexión a la base de datos cuando hayas terminado
    # db.close_connection()
    # print(db.search_player_by_id(1,0))