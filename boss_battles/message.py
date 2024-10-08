class InvalidMessageError(Exception):
    pass


class Message:
    user: str
    target: str
    action: str
    args: list[str]
    
    def __init__(self, s: str):
        """
        Validates and parses a string with the format:
        user_id@problem_id/cmd [arg[, arg...]]
        
        Args:
            s (str): The input string to validate.
            
        """
        # Find positions of '@' and '/'
        at_pos = s.find('@')
        slash_pos = s.find('/')
        
        # Check if both '@' and '/' are present and in the correct order
        if at_pos == -1 or slash_pos == -1 or at_pos > slash_pos:
            raise InvalidMessageError("InvalidMessageError - Invalid message format.")
            # return None  # Invalid format
        
        # Extract user_id and problem_id
        user = s[:at_pos]
        target = s[at_pos + 1:slash_pos]
        
        # Find the position of the first space after the command (if any)
        space_pos = s.find(' ', slash_pos)
        if space_pos == -1:
            # No arguments provided
            action = s[slash_pos + 1:]
            args_str = ''
        else:
            # Extract command and arguments string
            action = s[slash_pos + 1:space_pos]
            args_str = s[space_pos + 1:]
        
        # Validate that user_id, problem_id, and cmd are non-empty
        if not user or not target:
            raise InvalidMessageError("InvalidMessageError - Username and PID must not be empty.")
        
        # Optionally, validate that user_id, problem_id, and cmd are alphanumeric or underscores
        for component in [user, target, action]:
            if not component.replace('_', '').isalnum():
                raise InvalidMessageError("InvalidMessageError - Invalid characters. Must be letters and numbers only.")
        
        # Parse arguments into a list
        if args_str:
            # Split arguments by commas and strip whitespace
            args = [arg.strip() for arg in args_str.split(' ')]
            # Remove any empty strings from the list
            args = [arg for arg in args if arg]
        else:
            args = []

        self.user = user
        self.target = target
        self.action = action
        self.args = args

