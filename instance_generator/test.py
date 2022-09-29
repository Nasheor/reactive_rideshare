import codecs
import os

constraints= {
    'secs': [1, 2, 4, 8],
    'energy': [0.5, 1.0, 2.0, 6.0],
    'tps': [300, 1000],
    'ev_factor': [1.0, 2.0]
}


def main():
    parent_dir = './instances/evaluation_dynamic_ev/'
    for s in constraints['secs']:
        for energy in constraints['energy']:
            folder = str(s)+'_SEC_'+str(energy)+'_ENERGY'
            path = os.path.join(parent_dir, folder)
            os.mkdir(path)


if __name__ == '__main__':
    main()
