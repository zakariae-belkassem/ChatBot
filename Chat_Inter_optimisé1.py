import os
import openai
import mysql.connector

# Configuration de la clé API OpenAI
openai.api_key = open("Key", "r").read().strip()

# Configuration de la connexion MySQL
db_config = {
    'user': 'root',
    'password': 'root',  #entrer le mdps
    'host': 'localhost',
    'database': 'telecom_assistant',
}

# Connexion à la base de données MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


# Fonction pour insérer les offres si elles n'existent pas
def insert_offers():
    offers_data = [
        ("Forfait Illimité", "Appels illimités vers tous les réseaux, 50 Go de data.", "200 DH/mois"),
        ("Forfait International", "Appels vers l'international à tarif réduit, 10 Go de data.", "300 DH/mois"),
        ("Forfait Jeunes", "10 Go de data, SMS illimités.", "100 DH/mois"),
        ("Forfait Famille", "Partage de 100 Go de data, appels gratuits entre membres de la famille.", "500 DH/mois")
    ]
    cursor.execute('DELETE FROM offers')
    cursor.executemany('INSERT IGNORE INTO offers (name, description, price) VALUES (%s, %s, %s)', offers_data)
    conn.commit()


#fonction pour récupérer les messages commencant par qst
def getquestion():
    query = '''
                SELECT DISTINCT content
                FROM messages
                WHERE role = "user"
                LIMIT 50;
            '''
    cursor.execute(query)
    data = cursor.fetchall()
    simple_list = [item[0] for item in data]
    return simple_list


# Fonction pour récupérer les détails des offres depuis la base de données
def get_offer_details():
    cursor.execute('SELECT name, description, price FROM offers')
    return cursor.fetchall()


# Fonction pour insérer un message dans la base de données
def log_to_db(role, content, usr):
    cursor.execute('INSERT INTO messages (role, content,user_id) VALUES (%s, %s,%s)', (role, content, usr))
    conn.commit()


# Fonction de requête OpenAI
def Chat(user_messages) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=user_messages,
        temperature=1.2,
    )
    return response.choices[0].message['content']


# Fonction pour démarrer le chat
def startChat(user_message, Conn_userId):
    insert_offers()  # Initialiser les offres dans la base de données
    Topic = "offres de Maroc Telecom"
    all_messages = [{"role": "system",
                     "content": "Vous êtes un assistant de Maroc Telecom, vous pouvez uniquement répondre aux "
                                "questions relatives aux offres de Maroc Telecom"}]

    # Commande pour obtenir les détails des offres
    if any(word in user_message for word in ["tarifs", "détails", "offres", "offre", "tarif"]):
        offers = get_offer_details()
        if offers:
            response = "Voici les détails des offres de Maroc Telecom :\n" + "\n".join(
                f"Offre: {offer[0]}\nDescription: {offer[1]}\nPrix: {offer[2]}\n"
                for offer in offers
            )
        else:
            response = "Je n'ai pas d'informations sur les offres pour le moment."

        log_to_db('user', user_message, Conn_userId)
        log_to_db('assistant', response, Conn_userId)
        return response

    if user_message == "exit":
        return

    if user_message == "topic":
        print("Bot : Quel est le nouveau sujet sur lequel vous voulez discuter ?")
        Topic = input("Utilisateur : ").strip()
        os.system('cls' if os.name == 'nt' else 'clear')
        all_messages = [{"role": "system",
                         "content": f"Vous êtes un assistant pour les offres de Maroc Telecom, vous pouvez uniquement répondre aux questions relatives aux offres de Maroc Telecom"}]

        return

    all_messages.append({"role": "user", "content": user_message})
    log_to_db('user', user_message, Conn_userId)
    result = Chat(get_content_by_user_id(Conn_userId))
    all_messages.append({"role": "assistant", "content": result})
    log_to_db('assistant', result, Conn_userId)

    return result


#
# get the messages of the connected user
def get_content_by_user_id(user_id):
    # Define the query to select content column where user_id matches
    query = "SELECT content FROM messages WHERE user_id = %s ORDER BY date DESC"

    # Execute the query
    cursor.execute(query, (user_id,))

    # Fetch all the results
    content_list = [row[2] for row in cursor.fetchall()]

    return content_list[-4:]
