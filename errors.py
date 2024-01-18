class InvalidAspectRatio(Exception):
    def __init__(self, message):
        super().__init__("Invalid aspect ratio" + message)
        
class InvalidBountyNumber(Exception):
    def __init__(self):
        super().__init__("Invalid bounty number")