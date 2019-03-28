from __future__ import print_function

import os
import tensorflow as tf
import tensorflow.contrib.keras as kr

from utils import read_sentiment_category,  read_vocab
from model_stru import TCNNConfig, TextCNN


base_dir = 'data/sentiment_data'
vocab_dir = os.path.join(base_dir, 'cnews.vocab.txt')

save_dir = 'checkpoints/textcnn_20181224'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径


class SentimentModel(object):
    def __init__(self):
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_sentiment_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.config.num_classes = 3
        self.model = TextCNN(self.config)

        with self.model.graph.as_default():
            self.model.session.run(tf.global_variables_initializer())
            saver = tf.train.Saver()
            saver.restore(sess=self.model.session, save_path=save_path)  # 读取保存的模型

    def predict(self, content):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.model.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]

