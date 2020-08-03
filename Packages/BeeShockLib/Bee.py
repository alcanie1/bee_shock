class Bee(object):

    def __init__(self, name):
        self.bee_name = name
        self.frames_spent_on_yellow_area = 0
        self.frames_spent_on_blue_area = 0

    def __str__(self):
        fps = 30
        time_on_yellow_area = self.frames_spent_on_yellow_area / fps
        time_on_blue_area = self.frames_spent_on_blue_area / fps
        total_time = time_on_yellow_area + time_on_blue_area

        res = f'''  
            {self.bee_name} stats: 
        ======================================
          Time spent on yellow area: { time_on_yellow_area } seconds
          Time precentage on yellow area: { (time_on_yellow_area / total_time) * 100 }%
          Time spent on blue area: { time_on_blue_area } seconds
          Time precentage on blue area: { (time_on_blue_area / total_time) * 100 }% \n
          ''' 

        return res
