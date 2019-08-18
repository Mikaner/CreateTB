import os
import gzip
import numpy as np
import pickle
import matplotlib.pyplot as plt

dataset_dir = os.path.dirname(os.path.abspath(__file__))
save_file = dataset_dir + '/mnist.pkl'

key_file = {
    'train_img':'train-images-idx3-ubyte.gz',
    'train_label':'train-labels-idx1-ubyte.gz',
    'test_img':'t10k-images-idx3-ubyte.gz',
    'test_label':'t10k-labels-idx1-ubyte.gz'
}

def load_img(file_name):
    file_path = dataset_dir + '/' + file_name
    with gzip.open(file_path, 'rb') as f:
        data = np.frombuffer(f.read(), np.uint8, offset=16)
    data = data.reshape(-1, 28**2)
    
    return data

def load_label(file_name):
    file_path = dataset_dir + '/' + file_name
    with gzip.open(file_path, 'rb') as f:
        data = np.frombuffer(f.read(), np.uint8, offset=8)

    return data

def to_one_hot(label):
    T = np.zeros((label.size, 10))
    for i, row in enumerate(T):
        row[label[i]] = 1
    return T

def normalize(dataset):
    dataset = dataset.astype(np.float32)
    dataset /= 255

    return dataset

def save_mnist():
    dataset = {}
    dataset['train_img'] = load_img(key_file['train_img'])
    dataset['train_label'] = load_label(key_file['train_label'])
    dataset['test_img'] = load_img(key_file['test_img'])
    dataset['test_label'] = load_label(key_file['test_label'])

    with open(save_file, 'wb') as f:
        pickle.dump(dataset, f, -1)

def load_mnist(normalize=True, flatten=True, one_hot_label=False):
    with open(save_file, 'rb') as f:
        dataset = pickle.load(f)
    
    if normalize:
        for key in ('train_img', 'test_img'):
            dataset[key] = normalize(dataset[key])

    if one_hot_label:
        for key in ('train_label', 'test_label'):
            dataset[key] = to_one_hot(dataset[key])
    
    if not flatten:
        for key in ('train_img', 'test_img'):
            dataset[key] = dataset[key].reshape(-1,1,28,28)

    return (dataset['train_img'], dataset['train_label']) , (dataset['test_img'], dataset['test_label'])
