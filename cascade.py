from stage import Stage


class Cascade:

    def __init__(self, rect_shape, cent_params, flow, goal):
        """
        :param rect_shape:
        :param strip_shape:
        """
        if self.check_input(flow, goal):
            # print(f"The final waste of the process is ({flow[1] - goal[1]}, {round((flow[0] * flow[0] - goal[0] * goal[1]) / (flow[1] - goal[1]), 4)})")

            if cent_params[0] > 1:
                self.Q = cent_params[1]
                self.rectifier = [Stage(*cent_params, rect_shape[i]) for i in range(len(rect_shape))]
                # self.stripper = [Stage(*cent_params, strip_shape[i]) for i in range(len(strip_shape))]
                self.feed, self.n0 = flow
                self.breakout_time = 0
                self.total_product = 0
                self.conc_goal, self.amount_goal = goal

            else:
                raise ValueError("Alpha value must be bigger than 1!")

        else:
            raise ValueError("Not enough U-235 in the input stream, enrichment goal can't be achieved!")

    def check_input(self, flow, goal):
        return True
        return flow[0] * flow[1] > goal[0] * goal[1]

    def run(self):
        print("Cascade is running!")
        feed = self.feed
        concentration = self.n0
        product = 0
        # TODO:
        while self.total_product < self.amount_goal:
            for stage in self.rectifier:
                (product, n_product), (waste, n_waste) = stage.advance(feed, concentration)

                if n_product >= self.conc_goal:
                    time_to_reach = (self.amount_goal - self.total_product) / (product * self.Q)
                    self.breakout_time += time_to_reach
                    self.total_product += product * time_to_reach
                    return

                feed = waste
                concentration = n_waste

            # Update the total product and time elapsed per iteration
            self.total_product += product * self.Q  # TODO: number of centrifuges in the stage
            self.breakout_time += 1  # Iteration represents one unit time step


    def add_centrifuge(self):
        pass

    def change_centrifuge(self):
        pass