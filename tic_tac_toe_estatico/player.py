class Player:
    X = 0
    O = 1
    all_players = [X, O]


player_names = {
    Player.X: "x",
    Player.O: "o",
}


def other_player(player):
    if player == Player.X:
        return Player.O
    elif player == Player.O:
        return Player.X
