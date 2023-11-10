import streamlit as st
import pandas as pd
from pymongo import MongoClient

client=MongoClient("mongodb+srv://fiverrautomation:he3eyetR@cluster0.pshiyd4.mongodb.net/?retryWrites=true&w=majority")
db = client['ECHECS-ENSATÉ']
collection = db['Players-rating']

def calculate_new_rating(player_rating, opponent_rating, result, k_factor=16):
    expected_player_score = 1 / (1 + 10**((opponent_rating - player_rating) / 400))
    expected_opponent_score = 1 - expected_player_score

    new_rating = player_rating + k_factor * (result - expected_player_score)

    return new_rating

st.set_page_config(layout="wide") 

player_data = pd.read_excel('play.xlsx')
st.markdown("<h1 style='text-align: center; color: red;'>Chess Rating Manager</h1>", unsafe_allow_html=True)



st.header("Enter Match Details")
player1_name = st.selectbox("Player 1", player_data['FULL NAME'])
player2_name = st.selectbox("Player 2", player_data['FULL NAME'])
match_result = st.radio("Match Result", ("Player 1 wins", "Player 2 wins", "Draw"))

#sajal match result
if st.button("Submit Match Result"):

    if player1_name !=player2_name:
        player1 = player_data.loc[player_data['FULL NAME'] == player1_name]
        player2 = player_data.loc[player_data['FULL NAME'] == player2_name]
    
        if match_result == "Player 1 wins":
            white_result=1
            black_result=0
        elif match_result == "Player 2 wins":
            white_result=0
            black_result=1
        elif match_result=='Draw':
            white_result=0.5
            black_result=0.5
    
        new_player1_rating = calculate_new_rating(player1['ENSA RATING'].values[0], player2['ENSA RATING'].values[0], white_result)
        new_player2_rating = calculate_new_rating(player2['ENSA RATING'].values[0], player1['ENSA RATING'].values[0], black_result)
        p1=str(player1['FULL NAME'].values[0])
        st.write(f"the new rating of {player1['FULL NAME'].values[0]} is :\t{new_player1_rating}")
        st.write(f"the new rating of {player2['FULL NAME'].values[0]} is :\t{new_player2_rating}")

        player_data.loc[player_data['FULL NAME'] == player1['FULL NAME'].values[0], 'ENSA RATING'] = new_player1_rating
        player_data.loc[player_data['FULL NAME'] == player2['FULL NAME'].values[0], 'ENSA RATING'] = new_player2_rating

        
        # player_data.to_excel('chess_players.xlsx', index=False)
        player_data.to_excel("play.xlsx",sheet_name="ENSATE rating",index=False)
        # pls_data=player_data.to_dict("records")
        # collection.delete_many()
        # collection.insert_many(pls_data)
        st.success("Match result submitted!")
    elif player1_name ==player2_name:
        st.error("One player cannot play against himself and count it as a win 😅")
        # pls_data=player_data.to_dict("records")
        # collection.delete_many()
        # collection.insert_many(pls_data)

#zid la3ibin 
st.header("Add Players")
new_player_name = st.text_input("Full Name")
if st.button("Add Player"):
    if new_player_name:
        if new_player_name not in player_data['FULL NAME'].values:
            new_player_data = pd.DataFrame({'FULL NAME': [new_player_name], 'ENSA RATING': [1500]})
            player_data = player_data.append(new_player_data, ignore_index=True)
        elif new_player_name in player_data['FULL NAME'].values:
            st.warning(f"Player '{new_player_name}' already exists!")

        st.success(f"Player '{new_player_name}' added with a rating of 1500!")
        player_data.to_excel("play.xlsx",sheet_name="ENSATE rating",index=False)
        pls_data=player_data.to_dict("records")
        collection.delete_many()
        collection.insert_many(pls_data)

st.header("Player Standings")
# try:
#     ps=[]
#     for i in collection.find():
#         ps.append(i)
#     fullnames=[]
#     ensa_ratings=[]
#     for dictionnary in ps:
#         fullnames.append(dictionnary['FULL NAME'])
#         ensa_ratings.append(dictionnary['ENSA RATING'])
#     data={'FULL NAME':fullnames,'ENSA RATING':ensa_ratings}
#     df=pd.DataFrame(data)
#     if len(df)==0:
#         raise Exception
#     st.dataframe(df)
    
# except :
st.dataframe(player_data)

player_data.to_excel('chess_players.xlsx', index=False)

if st.button('Save changes'):
    player_data.to_excel("play.xlsx",sheet_name="ENSATE rating",index=False)
    pls_data=player_data.to_dict("records")
    collection.delete_many({})
    collection.insert_many(pls_data)
    st.success("Changes are saved successfully!")

    
