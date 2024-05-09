# Importar las librerías necesarias
import numpy as np
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import layers, models

import os


# Imprimir el directorio de trabajo actual
print(os.getcwd())

# Cargar los datos del conjunto KMNIST
# Asegúrate de que los datos están en el formato correcto y accesibles en la ruta especificada
(x_train, y_train), (x_test, y_test) = np.load('kmnist-train-imgs.npz'), np.load('kmnist-train-labels.npz')

# Preprocesar los datos: Normalizar y redimensionar para ajustar al modelo
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1)).astype('float32') / 255
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1)).astype('float32') / 255

# Convertir las etiquetas a formato one-hot
y_train = to_categorical(y_train, num_classes=10)
y_test = to_categorical(y_test, num_classes=10)

# Definir el modelo de la red neuronal
model = models.Sequential([
    layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(72, activation='relu'),
    layers.Dense(72, activation='relu'),
    layers.Dense(72, activation='relu'),
    layers.Dense(72, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Compilar el modelo
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Entrenar el modelo
model.fit(x_train, y_train, epochs=3, batch_size=128, validation_data=(x_test, y_test))

# Evaluar el modelo
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test accuracy: {test_acc}')

