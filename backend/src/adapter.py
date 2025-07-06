import requests
import csv


def fetch_thingspeak_data(api_key, results=50):
    """
    Fetch data from ThingSpeak API
    
    Args:
        api_key (str): ThingSpeak API key
        results (int): Number of results to fetch (default: 50)
    
    Returns:
        list: List of feed data or None if failed
    """
    try:
        response = requests.get(f"https://api.thingspeak.com/channels/2924635/feeds.json?api_key={api_key}&results={results}")
        
        if response.status_code == 200:
            return response.json().get("feeds", [])
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None


def save_data_to_csv(data, filename="output.csv"):
    """
    Save ThingSpeak data to CSV file
    
    Args:
        data (list): List of feed data
        filename (str): Output CSV filename
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if data and len(data) > 0:
            with open(filename, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Data has been written to {filename}")
            return True
        else:
            print("No data to save")
            return False
    except Exception as e:
        print(f"Error saving data: {str(e)}")
        return False


def process_thingspeak_data(data):
    """
    Process ThingSpeak data to extract sensor values
    
    Args:
        data (list): List of ThingSpeak feed data
    
    Returns:
        list: List of sensor values [MQ2, MQ3, MQ4, MQ6, MQ7, MQ135, TEMP, HUMI] or None if failed
    """
    if not data:
        return None
    
    # Get the latest entry
    latest_entry = data[-1]
    
    # Extract sensor values
    try:
        sensor_values = [
            float(latest_entry.get("field1", 0)),  # MQ2
            float(latest_entry.get("field2", 0)),  # MQ3
            float(latest_entry.get("field3", 0)),  # MQ4
            float(latest_entry.get("field4", 0)),  # MQ6
            float(latest_entry.get("field5", 0)),  # MQ7
            float(latest_entry.get("field6", 0)),  # MQ135
            float(latest_entry.get("field7", 0)),  # TEMP
            float(latest_entry.get("field8", 0))   # HUMI
        ]
        return sensor_values
    except (ValueError, TypeError) as e:
        print(f"Error processing sensor values: {str(e)}")
        return None


def fetch_and_save_data(api_key="RJNVLFM0O88JP765", results=50, filename="output.csv"):
    """
    Fetch data from ThingSpeak and save to CSV
    
    Args:
        api_key (str): ThingSpeak API key
        results (int): Number of results to fetch
        filename (str): Output CSV filename
    
    Returns:
        list: Fetched data or None if failed
    """
    data = fetch_thingspeak_data(api_key, results)
    if data:
        save_data_to_csv(data, filename)
    return data


# For backward compatibility when running directly
if __name__ == "__main__":
    api_key = "RJNVLFM0O88JP765"
    fetch_and_save_data(api_key)