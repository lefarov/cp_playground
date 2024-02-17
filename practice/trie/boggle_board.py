
def get_neighbor_positions(posi, posj, board):
	neighbor_positions = []

	for di in range(-1, 2):
		for dj in range(-1, 2):
			new_posi = min(max(0, posi + di), len(board) - 1)
			new_posj = min(max(0, posj + dj), len(board[new_posi]) - 1)

			neighbor_positions.append((
				board[new_posi][new_posj], new_posi, new_posj
			))

	return neighbor_positions


def dfs_word_search(
	prefix,
	posi,
	posj,
	visited_positions,
	current_trie_node,
	result,
	board,
):
	if "#" in current_trie_node:
		result.append(prefix)
		del current_trie_node["#"]

	visited_positions = visited_positions.copy()
	visited_positions.add((posi, posj))
	
	for ch_next, posi_next, posj_next in get_neighbor_positions(posi, posj, board):
		if (posi_next, posj_next) not in visited_positions:
			if ch_next in current_trie_node:
				dfs_word_search(
					prefix + ch_next, 
					posi_next, 
					posj_next, 
					visited_positions, 
					current_trie_node[ch_next],
					result,
					board,
				)


def boggleBoard(board, words):
    # Construct a words Trie
	words_trie = {}
	
	for word in words:
		current_trie_node = words_trie
		for ch in word:
			if ch not in current_trie_node:
				current_trie_node[ch] = {}
			
			current_trie_node = current_trie_node[ch]
		
		current_trie_node["#"] = True
	
	# Iterate over the board
	result = []
	for i, row in enumerate(board):
		for j, ch in enumerate(row):
			if ch in words_trie:
				visited_positions = set()
				dfs_word_search(
					ch, i, j, visited_positions, words_trie[ch], result, board
				)
			
	return result


input_data = {
  "board": [
    ["a", "b"],
    ["c", "d"]
  ],
  "words": ["abcd", "abdc", "acbd", "acdb", "adbc", "adcb", "abca"]
}

boggleBoard(**input_data)