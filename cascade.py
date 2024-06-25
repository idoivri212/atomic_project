from stage import Stage


class Cascade:

    def __init__(self, rect_shape, strip_shape, cent_params, flow):
        """
        :param rect_shape:
        :param strip_shape:
        """
        self.rectifier = [Stage(*cent_params, rect_shape[i]) for i in range(len(rect_shape))]
        self.stripper = [Stage(*cent_params, strip_shape[i]) for i in range(len(strip_shape))]
        self.flow = flow

    def run(self):
        print("Cascade is running!")

    def advance(self):
        pass

    def add_centrifuge(self):
        pass

    def change_centrifuge(self):
        pass