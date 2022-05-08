
action_space = []
# add every empty node to action space
for i in range(6):
    for j in range(6):
        if not self.board.is_occupied((i, j)):
            action_space.append((i, j))
if count_nonzero(self.board._data) == 0 and self.n % 2 == 1:
    action_space.remove((self.n // 2, self.n // 2))

best_score = float('-inf')
best_action = None
player = _TOKEN_MAP_IN[self.player]
for action in action_space:
    score = evaluation(self.board._data, self.n, player, action)
    if score > best_score:
        best_score = score
        best_action = action