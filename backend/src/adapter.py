import requests
import csv


def fetch_thingspeak_data(api_key, results=10):
    """
    Fetch data from ThingSpeak API
    
    Args:
        api_key (str): ThingSpeak API key
        results (int): Number of results to fetch (default: 50)
    
    Returns:
        list: List of feed data or None if failed
    """
    try:
        response = requests.get(f"https://api.thingspeak.com/channels/3018524/feeds.json?api_key={api_key}&results={results}")
        
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
    Process ThingSpeak data to extract array of sensor values
    
    Args:
        data (list): List of ThingSpeak feed data
    
    Returns:
        list: List of sensor data arrays [[MQ136, MQ137, TEMP, HUMI], ...] or None if failed
    """
    if not data:
        return None
    
    # Extract all valid sensor readings as array
    try:
        sensor_arrays = []
        
        # Map ThingSpeak fields to our sensors: MQ136, MQ137, TEMP, HUMI
        field_mapping = ["field1", "field2", "field3", "field4"]

        # Process each entry to get sensor values
        for entry in data:
            sensor_values = []
            has_valid_data = False
            
            for field_name in field_mapping:
                field_value = entry.get(field_name)
                if field_value is not None and field_value != "":
                    try:
                        value = float(field_value)
                        sensor_values.append(round(value, 2))
                        has_valid_data = True
                    except (ValueError, TypeError):
                        sensor_values.append(0.0)  # Default to 0 for invalid data
                else:
                    sensor_values.append(0.0)  # Default to 0 for missing data
            
            # Only add if we have at least some valid data
            if has_valid_data:
                sensor_arrays.append(sensor_values)
        
        print(f"Processed {len(sensor_arrays)} valid entries from {len(data)} total entries")
        return sensor_arrays
        
    except Exception as e:
        print(f"Error processing sensor values: {str(e)}")
        return None


def fetch_and_save_data(api_key="P91SEPV5ZZG00Y4S", results=50, filename="output.csv"):
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
    api_key = "P91SEPV5ZZG00Y4S"
    fetch_and_save_data(api_key)