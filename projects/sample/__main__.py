from tensorflow import keras
from utils import create_model, create_mnist_data
from os.path import dirname

# label, imageの順に格納されている
((train_labels, train_images), (test_labels, test_images)) = create_mnist_data()

# 基本的なモデルのインスタンスを作成
model = create_model()

# モデルの構造を表示
model.summary()

checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = dirname(checkpoint_path)

cp_callback = keras.callbacks.ModelCheckpoint(
    checkpoint_path,
    save_weights_only=True,
    verbose=1
    )

print(train_images.shape)

# モデルを訓練
model.fit(
        train_images,
        train_labels,
        epochs=10,
        validation_data=(test_images, test_labels),
        callbacks=[cp_callback]
    )
