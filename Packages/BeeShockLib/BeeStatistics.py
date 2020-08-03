from matplotlib import pyplot as plt
from matplotlib.ticker import ( MultipleLocator, FormatStrFormatter, AutoMinorLocator )
import numpy as np
from Packages.BeeShockLib import Bee


class BeeStatistics(object):
    
    def graph_bees_positions(self, bees_positions, GRAPH_DST_PATH, fig_size=None):

        if fig_size is None:
            fig_size = (10, 6)
        
        titles = [
            'Bee1 Trayectory', 'Bee2 Trayectory', 'Bee3 Trayectory', 'Bee4 Trayectory', 'Bee5 Trayectory',
        'Bee6 Trayectory', 'Bee7 Trayectory', 'Bee8 Trayectory', 'Bee9 Trayectory', 'Bee10 Trayectory'
        ] 
        
        fig, ax = plt.subplots(ncols=2, nrows=1, figsize=fig_size)
        
        i = 0
        j = 0
        for title, bee_positions in zip(titles, bees_positions):

            plt.sca(ax[i])
            plt.title(title)
            plt.plot(bee_positions)
            plt.plot((0, bee_positions.size), (150, 150), 'k--')
            ax[i].xaxis.set_major_locator(MultipleLocator(90))
            ax[i].xaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax[i].xaxis.set_minor_locator(MultipleLocator(30))

            if i == 1:
                i = 0
                j += 1
                plt.savefig(f'{GRAPH_DST_PATH}/figure{j}.jpeg')
                fig, ax = plt.subplots(ncols=2, nrows=1, figsize=fig_size)

            else:
                i += 1


    def compute_bee_statistics(self, bees_positions, STATS_DST_PATH):
        bees = self.__count_frames_spent_on_each_area(bees_positions)         
        self.__save_statistics(bees, STATS_DST_PATH)
        

    def __count_frames_spent_on_each_area(self, bees_positions):
        area_border = 150
        bees = []

        # This will do at most 90,000 iterations. 90,000 if the whole video was processed.
        for i, bee_positions in enumerate(bees_positions):
            
            bee_name = f'Bee{i+1}'
            bee = Bee.Bee(bee_name)

            for position in bee_positions:

                if position == 0:
                    # Do nothing with this value. position == 0 when bees are not being tracked. (power is off)
                    continue 

                elif position < area_border:
                    bee.frames_spent_on_blue_area += 1

                else:
                    bee.frames_spent_on_yellow_area += 1
            
            bees.append(bee)
        
        return bees

    
    def __save_statistics(self, bees, STATS_DST_PATH):

        with open(f'{STATS_DST_PATH}/statistics.txt', 'w') as output_file:

            output_file.write('::Bees Statistics After Power Is Turned On::\n')
            
            for bee in bees:
                output_file.write(bee.__str__())
