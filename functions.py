def summary_statistics(df):
    """
    Summary statistics for all variables in the DataFrame.

    Parameters:
        df (pd.DataFrame)
        

    Returns:
        pd.DataFrame: ummary statistics for all variables.
    """
    summary = df.describe(include='all')
    summary = summary.transpose()
    return summary


def missing_data(df):
    """
    Total and percentage of missing values for each column in the DataFrame.

    Parameters:
         df (pd.DataFrame)

    Returns:
        pd.DataFrame: DataFrame with two columns ('Total', 'Percent') showing the number and percentage of missing values.
    """
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum() / len(df)) * 100
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'], sort=False).sort_values('Total', ascending=False)
    return missing_data.head(150)

def get_random_color():
    return "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])


def routes_map(df, map):
    """
    Add routes to a given map based on grouped data.

    Parameters:
        df (pd.DataFrame): DataFrame containing latitude, longitude, and UnitNumber_masked
        map (folium.Map): Folium map object where routes and markers will be added.

    Returns:
        folium.Map: Updated map with routes and markers.
    """
    grouped = df.groupby('UnitNumber_masked')

    for name, group in grouped:
        coordinates = list(zip(group['General_Pos_Lat'], group['General_Pos_Long']))
        color = get_random_color()
        folium.PolyLine(coordinates, color=color, weight=2.5, opacity=1).add_to(map)
        for coord in coordinates:
            folium.Marker(location=coord).add_to(map)
    
    return map

#Take from http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def date_diff(df,start_time,end_time):
    """
    Calculate the difference start_time,end_time

    Parameters:
        df (pd.DataFrame)
        start_time 
        end_time

    Returns:
        DataFrame with an additional 'travel_time' column.
    """
    df[start_time] = pd.to_datetime(df[start_time])
    df[end_time] = pd.to_datetime(df[end_time])
    df['travel_time'] = df[end_time] - df[start_time]
    
    return df