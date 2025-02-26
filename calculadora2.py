import pandas as pd
from datetime import datetime

def add(a: float, b: float) -> float:
    """
    Adds two numbers and returns the result.
    
    Args:
        a (float): First number to add
        b (float): Second number to add
    
    Returns:
        float: The sum of a and b
    """
    return a + b

def create_operations_log(operations: list) -> pd.DataFrame:
    """
    Creates a DataFrame with mathematical operations and performs basic analysis.
    
    Args:
        operations (list): List of tuples containing (number1, number2, result)
    
    Returns:
        pd.DataFrame: DataFrame with the operations and analysis
    """
    # Create DataFrame
    df = pd.DataFrame(operations, columns=['Number1', 'Number2', 'Result'])
    
    # Add some interesting columns
    df['Operation_Date'] = datetime.now()
    df['Is_Result_Even'] = df['Result'] % 2 == 0
    df['Numbers_Sum_Greater_Than_10'] = df['Number1'] + df['Number2'] > 10
    
    # Calculate some statistics
    print("\nEstadísticas básicas:")
    print(df.describe())
    
    # Save to CSV
    df.to_csv('operations_log.csv', index=False)
    print("\nDatos guardados en 'operations_log.csv'")
    
    return df

# Usage example
if __name__ == "__main__":
    # Testing the basic add function
    result1 = add(5, 3)
    result2 = add(10.5, 4.5)
    
    print(f"Sum of 5 + 3 = {result1}")
    print(f"Sum of 10.5 + 4.5 = {result2}")
    
    # Testing pandas functionality
    operations_list = [
        (5, 3, result1),
        (10.5, 4.5, result2),
        (20, 30, add(20, 30)),
        (2.5, 7.5, add(2.5, 7.5)),
        (15, 25, add(15, 25))
    ]
    
    df = create_operations_log(operations_list)
    
    # Mostrar algunas funcionalidades útiles de pandas
    print("\nOperaciones donde el resultado es par:")
    print(df[df['Is_Result_Even']])
    
    print("\nOperaciones donde la suma es mayor que 10:")
    print(df[df['Numbers_Sum_Greater_Than_10']]) 