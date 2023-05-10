import time
from utils import create_mnist_data
from tensorflow import GradientTape
from tensorflow.keras import optimizers, losses, metrics, models
from tensorflow.data import Dataset

epochs = 2
batch_size = 64
buffer_size = 1024
log_step = 200
model_save_path = "../models/sample_py/example2.h5"
model_load_path = "../models/sample_py/example.h5"

optimizer = optimizers.SGD(learning_rate=1e-3)
loss_fn = losses.SparseCategoricalCrossentropy(from_logits=True)
train_acc_metric = metrics.SparseCategoricalAccuracy()
test_acc_metric = metrics.SparseCategoricalAccuracy()

# create models
model = models.load_model(model_load_path)
model.summary()

(train_labels, train_images), (test_labels, test_images) = create_mnist_data()

train_dataset = Dataset \
    .from_tensor_slices((train_images, train_labels)) \
    .shuffle(buffer_size=buffer_size) \
    .batch(batch_size)

test_dataset = Dataset \
    .from_tensor_slices((test_images, test_labels)) \
    .batch(batch_size)

for epoch in range(epochs):
    start_time = time.time()
    print(f"\n Start of epoch {(epoch, )}")
    for step, (x_batch_train, y_batch_train) in enumerate(train_dataset):
        print(f'x shape {x_batch_train.shape}')
        with GradientTape() as tape:
            logits = model(x_batch_train, training=True)
            loss_value = loss_fn(y_batch_train, logits)
        grads = tape.gradient(loss_value, model.trainable_weights)
        optimizer.apply_gradients(zip(grads, model.trainable_weights))

        train_acc_metric.update_state(y_batch_train, logits)

        if step % buffer_size == 0:
            print(f"training loss (for one batch) at step {step}: {float(loss_value):.4f}")
            print(f"Seen so far: {(step + 1) * batch_size} samples.")
    print(f"Time taken: {(time.time() - start_time):.2f}s")
    train_acc = train_acc_metric.result()
    train_acc_metric.reset_states()
    models.save_model(model, model_save_path)

