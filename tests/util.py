
def log(f):
    def f_(*args):
        pretty_list = f.func_name.split("_")[1:]
        prettier_list = list()
        for word in pretty_list:
            word_list = list(word)
            word_list[0] = word[0].upper()
            prettier_list.append("".join(word_list))

        print "===", " ".join(prettier_list), "==="
        return f(*args)

    return f_
