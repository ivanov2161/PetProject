def _increase_word_count(word_learned) -> None:
    """Increase word counter after right answer"""

    if word_learned == 0:
        print('0')
    elif word_learned < 7:
        print('1')

    elif word_learned >= 7:
        print('2')



# _increase_word_count(0)
# _increase_word_count(5)
_increase_word_count(7)
# _increase_word_count(8)