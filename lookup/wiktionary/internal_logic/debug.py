def debug_print_matching(set_a, set_b, full_a, full_b, one_side_a, one_side_b):
    print('----Debug Matching: Answers set------')
    for key, value in set_a.items():
        print('{}:{} => {}'.format(key.wiki_title, key.part_of_speech.name,
                                   ''.join(map(lambda x: '\n  {}'.format(x), value))))
    print('----Debug Matching: Questions set------')
    for key, value in set_b.items():
        print('{}:{} => {}'.format(key.wiki_title, key.part_of_speech.name,
                                   ''.join(map(lambda x: '\n  {}'.format(x), value))))
    if full_a:
        print('----Debug Matching: Full from answer------')
        print('\n'.join(map(str, full_a)))
    if full_b:
        print('----Debug Matching: Full from question------')
        print('\n'.join(map(str, full_b)))
    if one_side_a:
        print('----Debug Matching: One-side from answer------')
        print('\n'.join(map(str, one_side_a)))
    if one_side_b:
        print('----Debug Matching: One-side from question------')
        print('\n'.join(map(str, one_side_b)))
