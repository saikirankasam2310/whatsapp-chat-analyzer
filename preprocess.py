import re
import pandas as pd

def preprocess(data):
    """
    Preprocess WhatsApp chat export into a structured DataFrame.
    Supports multiple timestamp formats (12hr, 24hr, DD/MM/YYYY, MM/DD/YYYY).
    """

    # UNIVERSAL REGEX → supports both 12-hour & 24-hour formats
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}(?:\s?[apAP][mM])?) - '

    # Split data into parts → [date, time, message]
    messages = re.split(pattern, data)

    # If parsing failed, return empty dataframe
    if len(messages) < 3:
        return pd.DataFrame(columns=["date", "user", "message", "year", "month", "day", "day_name", "hour", "minute"])

    dates = []
    texts = []
    senders = []

    # Start at index 1 because regex splits into chunks: [unused, date, time, message]
    for i in range(1, len(messages), 3):
        date = messages[i]
        time = messages[i + 1]
        message_block = messages[i + 2]

        # Combine date + time into one string
        full_datetime = f"{date}, {time}"
        content = message_block.split(": ", 1)

        # Separate sender vs system message
        if len(content) == 2:
            senders.append(content[0])
            texts.append(content[1])
        else:
            senders.append("group_notification")
            texts.append(content[0])

        dates.append(full_datetime)

    # Build DataFrame
    df = pd.DataFrame({"date": dates, "user": senders, "message": texts})

    # Convert "date" into proper datetime → handles 12hr + 24hr
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

    # Drop rows where datetime failed
    df = df.dropna(subset=["date"])

    # Extract components for timeline analysis
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    return df
