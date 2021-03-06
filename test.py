from PIL import Image
import tensorflow as tf


class Test():
    def __init__(self,picspath):
        self.x = tf.placeholder(tf.float32, [None, 784])

        self.y_ = tf.placeholder(tf.float32, [None, 10])

        self.path=picspath

    def imageprepare(self):
        im = Image.open(self.path) #读取的图片所在路径，注意是28*28像素
        # plt.imshow(im)  #显示需要识别的图片
        # plt.show()
        im = im.convert('L')
        tv = list(im.getdata())
        tva = [(255-x)*1.0/255.0 for x in tv]
        return tva


    def weight_variable(slef,shape):
        initial = tf.truncated_normal(shape,stddev = 0.1)
        return tf.Variable(initial)

    def bias_variable(slef,shape):
        initial = tf.constant(0.1,shape = shape)
        return tf.Variable(initial)

    def conv2d(self,x,W):
        return tf.nn.conv2d(x, W, strides = [1,1,1,1], padding = 'SAME')

    def max_pool_2x2(self,x):
        return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

    def work(self):
        W_conv1 = self.weight_variable([5, 5, 1, 32])
        b_conv1 = self.bias_variable([32])

        x_image = tf.reshape(self.x,[-1,28,28,1])

        h_conv1 = tf.nn.relu(self.conv2d(x_image,W_conv1) + b_conv1)
        h_pool1 = self.max_pool_2x2(h_conv1)

        W_conv2 = self.weight_variable([5, 5, 32, 64])
        b_conv2 = self.bias_variable([64])

        h_conv2 = tf.nn.relu(self.conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = self.max_pool_2x2(h_conv2)

        W_fc1 = self.weight_variable([7 * 7 * 64, 1024])
        b_fc1 = self.bias_variable([1024])

        h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

        keep_prob = tf.placeholder("float")
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

        W_fc2 = self.weight_variable([1024, 10])
        b_fc2 = self.bias_variable([10])

        y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

        cross_entropy = -tf.reduce_sum(self.y_*tf.log(y_conv))
        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
        correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(self.y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        saver = tf.train.Saver()
        result = self.imageprepare()
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver.restore(sess, '/Users/Sixuan/Desktop/pycharm/model.ckpt') #使用模型，参数和之前的代码保持一致

            prediction=tf.argmax(y_conv,1)
            predint=prediction.eval(feed_dict={self.x: [result],keep_prob: 1.0}, session=sess)

            print(predint[0])
            return predint[0]
