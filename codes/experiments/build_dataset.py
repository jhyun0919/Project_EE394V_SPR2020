from discover_mass import *
import pickle
import os


def build_dataset_for_learning(opf_data_dict,
                               test_cases,
                               alpha=0.05,
                               epsilon=0.04,
                               delta=0.01,
                               gamma=2,
                               mu=0,
                               std_scaler=0.03):
    dataset = {}

    for case_name in test_cases:
        print("> {}".format(case_name))
        # select dataset
        opf_data = opf_data_dict[case_name]
        
        # DiscoverMass
        discovered_active_sets, W, M, R_discovery = discover_mass(
            alpha, epsilon, delta, gamma, mu, std_scaler, opf_data)
        
        # store pre-processed dataset
        dataset[case_name] = {
            'x': W,
            'y': discovered_active_sets
        }
        
        # save dataset
        file_name = case_name.split(".")[0]
        current_path = os.getcwd()
        
        file_path = current_path + '/dataset/' + file_name + '.pickle'
        outfile = open(file_path,'wb')
        pickle.dump(opf_data_dict, outfile)
        outfile.close()
        
        # save dist plot
        filepath = current_path + '/plot_figures/' + filename + '.png'
        plot_active_set_dist(discovered_active_sets, filepath)