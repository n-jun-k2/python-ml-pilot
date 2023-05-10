from tensorflow import keras


def create_mnist_data():
    (train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

    train_labels = train_labels[:1000]
    test_labels = test_labels[:1000]

    train_images = train_images[:1000].reshape(-1, 28 * 28) / 255.0
    test_images = test_images[:1000].reshape(-1, 28 * 28) / 255.0

    return (train_labels, train_images), (test_labels, test_images)
