
def randomise(df, calendar):
    """
    Selects a random film from the dataframe that has not already
    been chosen in the Advent calendar.

    :param df: Dataframe containing the cleaned movie dataset
    :param calendar: list of dataframe indices that have already been picked
    :return: returns a single row dataframe of the selected film
    """
    remaining = df[~df.index.isin(calendar)]

    if remaining.empty:
        return None

    film = remaining.sample(1)

    return film
