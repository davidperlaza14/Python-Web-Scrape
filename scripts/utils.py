import logging

def setup_logging(log_file):
    """
    Sets up logging.
    
    Args:
    log_file (str): Path to the file where logs will be saved.
    """
    # Configure logging with a file, file mode, format, and logging level.
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.info("Logger configured")  

def save_to_csv(data, filename):
    """
    Saves data to a CSV file.
    
    Args:
    data (list of dict): Data to save.
    filename (str): Name of the CSV file.
    """
    import pandas as pd
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    logging.info(f"Data saved to {filename}")
