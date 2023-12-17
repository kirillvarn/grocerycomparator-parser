def cast_to_numeric(castable):
    try:
        return float(castable)
    except Exception as e:
        print(e)
        return 0
