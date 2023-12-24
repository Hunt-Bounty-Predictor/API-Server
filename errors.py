class InvalidAspectRatio(Exception):
    def __init__(self):
        super().__init__("Invalid aspect ratio")