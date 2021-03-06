from __future__ import division, print_function, absolute_import

import os

import tflearn
import tflearn.datasets.oxflower17 as oxflower17
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization


def alex_net():
    # 输入数据
    network = input_data(shape=[None, 227, 227, 3])
    # 第一层卷积
    network = conv_2d(network, 96, 11, strides=4, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    # 第二层卷积
    network = conv_2d(network, 256, 5, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    # 第三层卷积
    network = conv_2d(network, 384, 3, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    # 第四层卷积
    network = conv_2d(network, 384, 3, activation='relu')
    # 第五层卷积
    network = conv_2d(network, 256, 3, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    # 全连接层1
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    # 全连接层2
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    # 输出层
    network = fully_connected(network, 17, activation='softmax')
    network = regression(network, optimizer='momentum', loss='categorical_crossentropy', learning_rate=0.001)
    return network


if __name__ == '__main__':
    # 加载数据
    dataset = 'alexnet_oxflower17'
    X, Y = oxflower17.load_data(dirname='../datasets/17flowers', one_hot=True, resize_pics=(227, 227))
    # 构建模型
    alexnet = alex_net()
    modal = tflearn.DNN(alexnet, checkpoint_path='./model/', max_checkpoints=1, tensorboard_verbose=2)
    # 检查点
    model_file = './model/' + dataset + '.model'
    if os.path.isfile(model_file):
        modal.load(model_file)
    try:
        modal.fit(X, Y, n_epoch=10, validation_set=0.2, shuffle=True,
                  show_metric=True, batch_size=16, snapshot_step=200,
                  snapshot_epoch=True, run_id=dataset)
        modal.save(model_file)
    except KeyboardInterrupt as i:
        print('Closed by an KeyboardInterrupt')
    finally:
        modal.save(model_file)
