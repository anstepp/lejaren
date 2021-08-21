class MeterNode(Node):
    def __init__(self, Note):
        if Note.measure_flag == False:
            print("Node must be measure")
