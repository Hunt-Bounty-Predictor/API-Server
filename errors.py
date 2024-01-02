class InvalidAspectRatio(Exception):
    def __init__(self):
        super().__init__("Invalid aspect ratio")
        
class InvalidBountyNumber(Exception):
    def __init__(self):
        super().__init__("Invalid bounty number")