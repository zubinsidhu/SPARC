import os

def create_folder(folder_name, chat_history_file):
    """
    Creates a project folder and a text file to store chat history.

    Args:
        folder_name (str): The name of the project folder to create.
    """

    try:
        # Create the project folder
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            file_path = os.path.join(folder_name, chat_history_file)
            with open(file_path, 'w') as f:
                f.write("Chat history will be stored here.\n")
            return(f"Project folder '{folder_name}' created successfully.")
        else:
            return(f"Project folder '{folder_name}' already exists.")

        # Create the chat history file inside the project folder
        

    except OSError as e:
        return(f"Error creating project folder or file: {e}")

if __name__ == "__main__":
    create_folder(folder_name="", chat_history_file="")
