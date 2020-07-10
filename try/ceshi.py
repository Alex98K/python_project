def condition_author(author):  # 作者是谁或者不能是谁，才下载
    author_pass_down_list = []
    author_keep_down_word = '张婉芳'
    if author not in author_pass_down_list:
        if len(author_keep_down_word) > 0 and author_keep_down_word in author:
            return True
        elif len(author_keep_down_word) == 0:
            return True
        else:
            return False
    else:
        return False


print(condition_author('张婉'))