import config
import tensorflow as tf
import tensorflow.contrib.slim as slim

class Model_Lenet:

    def __init__(self, is_train=True):

        self.input_image = tf.placeholder(tf.float32, [None, 28, 28, 3])
        self.images = tf.reshape(self.input_image, [-1, 28, 28, 3])
        self.input_label = tf.placeholder(tf.float32, [None, 10])
        self.labels = tf.cast(self.input_label, tf.int32)
        self.global_step = tf.Variable(0.0, trainable=False, dtype=tf.float32)

        self.num_sample = config.num_sample
        self.batch_size = config.batch_size
        self.learning_rate = config.learning_rate
        
        with tf.variable_scope("Lenet") as scope:
            self.train_digits = self.build(True)
            scope.reuse_variables()
            self.pred_digits = self.build(False)

        self.prediction = tf.argmax(self.pred_digits, 1)
        self.correct_prediction = tf.equal(tf.argmax(self.pred_digits, 1), tf.argmax(self.labels, 1))
        self.train_accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, "float"))

        self.loss = slim.losses.softmax_cross_entropy(self.train_digits, self.labels)
        self.lr = tf.train.exponential_decay(self.learning_rate, self.global_step,
         (self.num_sample // self.batch_size) * config.epoch_decay, config.learning_decay, staircase=True)
        self.train_op = tf.train.MomentumOptimizer(self.lr, config.momentum).minimize(self.loss, global_step=self.global_step)


    def build(self, is_train=True):

        with slim.arg_scope([slim.conv2d], padding='VALID'):
            net = slim.conv2d(self.images, 32, [5,5], 1, padding='SAME', activation_fn=tf.nn.relu, scope='conv1')
            net = slim.max_pool2d(net, [2, 2], scope='pool2')
            net = slim.conv2d(net, 32, [5,5], 1, padding='SAME', activation_fn=tf.nn.relu, scope='conv3')
            net = slim.max_pool2d(net, [2, 2], scope='pool4')
            net = slim.conv2d(net, 64, [5,5], 1, padding='SAME', activation_fn=tf.nn.relu, scope='conv5')
            net = slim.flatten(net, scope='flat6')
            net = slim.fully_connected(net, 4096, activation_fn=tf.nn.relu, scope='fc7')
            net = slim.dropout(net, 0.5, is_training=is_train)
            digits = slim.fully_connected(net, 10, scope='fc8')
        return digits

