import tensorflow as tf
import pandas as pd
import numpy as np
from ClientClassification import loadData

def trainData():
    #需要转换成onehot类型数据
    data = pd.read_csv("onehot.csv",).values.astype(np.float32)  #load Data to numpy
    np.random.shuffle(data)
    sep = int(0.7*len(data))
    train_data = data[:sep]
    test_data = data[sep:]

    #tf load
    tf_input = tf.compat.v1.placeholder(tf.float32,[None,35],name="input")
    train_x = train_data[:,:33]
    train_y = train_data[:,33:]

    l1 = tf.layers.dense(train_x,128,tf.nn.relu,name="l1")
    l2 = tf.layers.dense(l1,128,tf.nn.relu,name="l2")
    out = tf.layers.dense(l2,2,name="out")
    predict = tf.nn.softmax(out,name="predict")

    loss = tf.losses.softmax_cross_entropy(onehot_labels=train_y,logits=out)
    accuracy = tf.metrics.accuracy(labels=tf.nn.softmax(train_y,axis=1),
                                   predictions=tf.nn.softmax(out,axis=1))[1]

    opt = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=0.1)
    train_op = opt.minimize(loss)

    #saver
    # saver = tf.train.Saver()

    #intialize
    sess = tf.compat.v1.Session()
    sess.run(tf.group(tf.compat.v1.global_variables_initializer(),tf.compat.v1.local_variables_initializer()))

    for t in range(100):
        # training
        batch_index = np.random.randint(len(train_data), size=32)
        sess.run(train_op, feed_dict = {tf_input: train_data[batch_index]})

        print(out)
        # if t % 5 == 0:
        #     # testing
        #     acc_, pred_,= sess.run([accuracy, predict], {tf_input: test_data})
        #     print("Step: %i" % t, "| Accurate: %.2f" % acc_,  )
    # saver.save(sess,"net.ckpt")
    sess.close()


    pass

def load_syntax():
    W = tf.Variable(np.arange(33))
    saver = tf.train.Saver()
    saver.restore()
    pass

if __name__=="__main__":
    # trainData()
    pass

