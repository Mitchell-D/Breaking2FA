letters = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}
numbers = set(map(str, set(range(10))))
special = {"!", "@", "#", "$", "%", "&"}

def pass_info(passfile):
    with open(passfile, "r", encoding="ISO-8859-1") as pffp:
        lines = list(map(lambda a: a.replace("\n", ""), pffp.readlines()))

    print(f"Total passwords: {len(lines)}")
    contains_password = list(filter(
        lambda a: "password" in a.lower(),
        lines
        ))
    print(contains_password[:20])
    print(f"Passwords with 'password' as a substring: {len(contains_password)}\
            {len(contains_password)/len(lines)}% of total.")

    contains_constraints = list(filter(full_validation, lines))
    print(contains_constraints[:20])

    print(f"Passwords with all 3 constraints: {len(contains_constraints)}\
            {len(contains_constraints)/len(lines)}% of total.")

def full_validation(password):
    """
    Returns True if the password has at least one letter, number,
    and special character.
    """
    password = password.lower()
    let = letters.intersection(set(password))
    num = numbers.intersection(set(password))
    spec = special.intersection(set(password))
    # if len(spec): print(password, let, num)
    has_all = bool(len(let)) and bool(len(num)) and bool(len(spec))
    #if has_all: print(password)
    return has_all

if __name__=="__main__":
    passfile = "rockyou.txt"
    pass_info(passfile)
