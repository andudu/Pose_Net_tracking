import numpy as np
import operator

class tracking(object):

    def __init__(self):

        self.previous_dict = {}
        self.current_dict = {}
        self.return_dict = {}

    def return_most_similar(self,current_keypoints):

        # Intializes the prev dictionary with persons and all of their keep points
        if not self.previous_dict:
            for ii, keypoint in current_keypoints.items():
                temp_current = []
                temp_current.append(keypoint[0][5])
                temp_current.append(keypoint[0][6])
                temp_current.append(keypoint[0][11])
                temp_current.append(keypoint[0][12])
                self.previous_dict[ii] = temp_current
                self.return_dict[ii] = [

                    keypoint[0], #coordinats
                    keypoint[1], #keypoint
                    keypoint[2], #confidence_score
                    ii
                ]
        # Create a dictionary of only relevant keypoints for similarity testing
        else:
            for ii, keypoints in current_keypoints.items():
                temp_current = []
                temp_current.append(keypoints[0][5])
                temp_current.append(keypoints[0][6])
                temp_current.append(keypoints[0][11])
                temp_current.append(keypoints[0][12])
                current_keypoints[ii] = temp_current
            all_sim_indices = []
            for index, keypoints in self.previous_dict.items():
                similarity_scores = {}
                # Calculate the similarity score all individuals compared to currented person
                for current_index, current_keypoints in current_keypoints.items():
                    print('looped')
                    similarity_scores[current_index] = self.calculate_similarity(keypoints, current_keypoints)
                # The current frame's individual with the most similar keypoint score gets
                # assigned accordingly to master individual list
                print(similarity_scores)
                most_sim_index = min(similarity_scores.items(), key=operator.itemgetter(1))[0]
                self.previous_dict[index] = current_keypoints[most_sim_index]
                all_sim_indices.append(most_sim_index)
            for i, index in enumerate(all_sim_indices):
                self.return_dict[i] = [
                    current_keypoints[index][0],
                    current_keypoints[index][1],
                    current_keypoints[index][2],
                    index
                ]
        return self.return_dict

    def calculate_similarity(self, previous_keypoints, current_keypoints):
        diff = [current_keypoints[a] - previous_keypoints[a] for a in range(4)]
        return np.linalg.norm(diff)
