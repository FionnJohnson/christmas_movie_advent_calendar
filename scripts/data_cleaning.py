import pandas as pd

# --- Cleaning the data, removing unnecessary columns and filtering based on rating, number of votes and type

raw_data = pd.read_csv('../data/christmas_movies.csv')

# Selecting only the relevant columns and removing any rows with null values in these columns.
required_cols = 'title rating runtime imdb_rating genre release_year description director votes stars type'.split()
updated_data = raw_data.dropna(subset = required_cols)[required_cols]


# Filtering the data to only include films (rows) with type Movie, a rating >= 6.0 and 5000 votes or higher
updated_data['votes'] = (
    updated_data['votes']
    .str.replace(",", "", regex=False)
    .astype(int)
)

filtered_data = updated_data[
    (updated_data['type'] == 'Movie') &
    (updated_data['imdb_rating'] >= 6.0) &
    (updated_data['votes'] >= 5000) ].copy()

filtered_data['release_year'] = filtered_data['release_year'].apply(int)


# Changing the time format minutes to hrs and minutes
def format_runtime(minutes):
    
    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours == 0:
        return f"{int(minutes)} mins"
    elif remaining_minutes == 0:
        return f"{int(int(hours))}hrs"
    else:
        return f"{int(hours)}hr {int(remaining_minutes)} mins"

filtered_data['runtime'] = filtered_data['runtime'].apply(format_runtime)

# Saving the final dataset
filtered_data.to_csv('../data/cleaned_movies.csv', index=False)

